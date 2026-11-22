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
                 web_search: bool = False) -> LLMResult: ...

FALLBACK_BETA = "server-side-fallback-2026-07-01"

class ClaudeLLM:
    def __init__(self, cfg: dict):
        import anthropic  # reads ANTHROPIC_API_KEY from env (.env loaded by cli)
        self.client = anthropic.Anthropic()
        self.cfg = cfg

    def _cost(self, u: dict) -> float:
        p = self.cfg["pricing_per_mtok"]
        return (u["input"] * p["input"] + u["output"] * p["output"]
                + u["cache_read"] * p["cache_read"] + u["cache_write"] * p["cache_write"]) / 1e6

    def complete(self, *, role, system, task, max_tokens, web_search=False) -> LLMResult:
        cfg = self.cfg
        max_tokens = min(max_tokens, cfg["budget"]["per_call_max_output_tokens"])
        kw = dict(
            model=cfg["model"], max_tokens=max_tokens,
            # stable role instructions first + cache breakpoint; volatile task goes in the user turn
            system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral", "ttl": "1h"}}],
            thinking={"type": "adaptive"},
            output_config={"effort": cfg["effort"]},
        )
        betas = []
        if cfg.get("fallbacks"):
            betas.append(FALLBACK_BETA)
            kw["fallbacks"] = cfg["fallbacks"]
        if betas:
            kw["betas"] = betas
        if web_search:
            kw["tools"] = [{"type": "web_search_20260209", "name": "web_search",
                            "max_uses": cfg["round"]["literature_max_searches"]}]
        messages = [{"role": "user", "content": task}]
        usage = dict(input=0, output=0, cache_read=0, cache_write=0)
        texts, stop, model, details = [], "end_turn", cfg["model"], ""
        for _ in range(6):                      # pause_turn continuations for server tools
            with self.client.beta.messages.stream(messages=messages, **kw) as s:
                msg = s.get_final_message()
            u = msg.usage
            usage["input"] += u.input_tokens or 0
            usage["output"] += u.output_tokens or 0
            usage["cache_read"] += getattr(u, "cache_read_input_tokens", 0) or 0
            usage["cache_write"] += getattr(u, "cache_creation_input_tokens", 0) or 0
            texts += [b.text for b in msg.content if b.type == "text"]
            stop, model = msg.stop_reason, msg.model
            if getattr(msg, "stop_details", None):
                details = str(msg.stop_details)
            if stop != "pause_turn":
                break
            messages.append({"role": "assistant", "content": [b.model_dump(exclude_none=True) for b in msg.content]})
        return LLMResult("".join(texts), stop, model, usage, self._cost(usage), details)
