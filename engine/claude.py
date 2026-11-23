"""Thin Claude wrapper: streaming, adaptive thinking, prompt caching, refusal fallback, budget accounting."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Protocol

@dataclass
class LLMResult:
    text: str
    stop_reason: str = "end_turn"
    model: str = ""
    usage: dict = field(default_factory=dict)
    cost_usd: float = 0.0
    stop_details: str = ""

    @property
    def refused(self):
        return self.stop_reason == "refusal"

class LLM(Protocol):
    def complete(self, *, role: str, system: str, task: str, max_tokens: int,
                 web_search: bool = False, **kw) -> LLMResult: ...

FALLBACK_BETA = "server-side-fallback-2026-07-01"

class ClaudeLLM:
    def __init__(self, cfg: dict):
        import anthropic  # reads ANTHROPIC_API_KEY from env (.env loaded by cli)
        self.client = anthropic.Anthropic()
        self.cfg = cfg

    def role_cfg(self, role):
        r = (self.cfg.get("roles") or {}).get(role, {})
        return r.get("model", self.cfg["model"]), r.get("effort", self.cfg["effort"])

    def _cost(self, u: dict, model: str) -> float:
        p = (self.cfg.get("pricing") or {}).get(model) or self.cfg["pricing_per_mtok"]
        return (u["input"] * p["input"] + u["output"] * p["output"]
                + u["cache_read"] * p["cache_read"] + u["cache_write"] * p["cache_write"]) / 1e6

    def _stream_with_retry(self, messages, kw, attempts=3):
        """Mid-stream connection resets are not retried by the SDK; a long call must not die on one."""
        import time, anthropic
        for k in range(attempts):
            try:
                with self.client.beta.messages.stream(messages=messages, **kw) as s:
                    return s.get_final_message()
            except (anthropic.APIConnectionError, anthropic.APITimeoutError, anthropic.InternalServerError) as e:
                if k == attempts - 1:
                    raise
                time.sleep(5 * (k + 1))
            except Exception as e:                           # httpx2 transport errors surface unwrapped mid-stream
                if "httpx2" not in type(e).__module__ or k == attempts - 1:
                    raise
                time.sleep(5 * (k + 1))

    def complete(self, *, role, system, task, max_tokens, web_search=False, model=None, effort=None, task_budget=None, **_) -> LLMResult:
        cfg = self.cfg
        max_tokens = min(max_tokens, cfg["budget"]["per_call_max_output_tokens"])
        m0, e0 = self.role_cfg(role)
        model, effort = model or m0, effort or e0
        kw = dict(
            model=model, max_tokens=max_tokens,
            # stable role instructions first + cache breakpoint; volatile task goes in the user turn
            system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral", "ttl": "1h"}}],
            thinking={"type": "adaptive"},
            output_config={"effort": effort},
        )
        betas = []
        tb = task_budget if task_budget is not None else (cfg.get("task_budget") or {}).get(role)
        if tb:   # tells the model its token ceiling so it paces thinking and finishes with output instead of starving
            betas.append("task-budgets-2026-03-13")
            kw["output_config"] = {**kw["output_config"], "task_budget": {"type": "tokens", "total": tb}}
        if cfg.get("fallbacks") and "haiku" not in model:   # no server-side fallback for Haiku
            betas.append(FALLBACK_BETA)
            kw["fallbacks"] = cfg["fallbacks"]
        if betas:
            kw["betas"] = betas
        extra = (cfg.get("tools") or {}).get(role)
        if extra:
            kw["tools"] = list(extra)                       # e.g. server-side code execution for the prover
        if web_search:
            kw["tools"] = [{"type": "web_search_20260209", "name": "web_search",
                            "max_uses": cfg["round"]["literature_max_searches"]}]
        messages = [{"role": "user", "content": task}]
        usage = dict(input=0, output=0, cache_read=0, cache_write=0)
        texts, stop, details = [], "end_turn", ""
        for _ in range(6):                      # pause_turn continuations for server tools
            msg = self._stream_with_retry(messages, kw)
            u = msg.usage
            usage["input"] += u.input_tokens or 0
            usage["output"] += u.output_tokens or 0
            usage["cache_read"] += getattr(u, "cache_read_input_tokens", 0) or 0
            usage["cache_write"] += getattr(u, "cache_creation_input_tokens", 0) or 0
            texts += [b.text for b in msg.content if b.type == "text"]
            stop, model = msg.stop_reason, msg.model or model
            if getattr(msg, "stop_details", None):
                details = str(msg.stop_details)
            if stop != "pause_turn":
                break
            messages.append({"role": "assistant", "content": [b.model_dump(exclude_none=True) for b in msg.content]})
        return LLMResult("".join(texts), stop, model, usage, self._cost(usage, model), details)
