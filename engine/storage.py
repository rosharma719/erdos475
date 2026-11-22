"""SQLite bookkeeping for runs, calls, token usage and budgets. Math lives in Markdown/YAML, not here."""
from __future__ import annotations
import sqlite3, time
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS runs(
  id TEXT PRIMARY KEY, contract TEXT, programme TEXT, status TEXT, started REAL, finished REAL, outcome TEXT);
CREATE TABLE IF NOT EXISTS calls(
  id INTEGER PRIMARY KEY AUTOINCREMENT, run_id TEXT, role TEXT, model TEXT, ts REAL,
  input_tokens INT, output_tokens INT, cache_read INT, cache_write INT, cost_usd REAL, stop_reason TEXT);
"""

class BudgetExceeded(RuntimeError):
    pass

class Storage:
    def __init__(self, path: str | Path):
        self.db = sqlite3.connect(str(path))
        self.db.executescript(SCHEMA)

    def start_run(self, run_id, contract, programme):
        self.db.execute("INSERT OR IGNORE INTO runs VALUES(?,?,?,?,?,NULL,NULL)",
                        (run_id, contract, programme, "running", time.time()))
        self.db.commit()

    def finish_run(self, run_id, status, outcome=""):
        self.db.execute("UPDATE runs SET status=?, finished=?, outcome=? WHERE id=?",
                        (status, time.time(), outcome, run_id))
        self.db.commit()

    def record_call(self, run_id, role, model, usage: dict, cost, stop_reason):
        self.db.execute(
            "INSERT INTO calls(run_id,role,model,ts,input_tokens,output_tokens,cache_read,cache_write,cost_usd,stop_reason)"
            " VALUES(?,?,?,?,?,?,?,?,?,?)",
            (run_id, role, model, time.time(), usage.get("input", 0), usage.get("output", 0),
             usage.get("cache_read", 0), usage.get("cache_write", 0), cost, stop_reason))
        self.db.commit()

    def spent(self, run_id: str | None = None) -> float:
        q, a = ("SELECT COALESCE(SUM(cost_usd),0) FROM calls", ())
        if run_id:
            q, a = (q + " WHERE run_id=?", (run_id,))
        return float(self.db.execute(q, a).fetchone()[0])

    def check_budget(self, run_id, per_round, total):
        if self.spent(run_id) >= per_round:
            raise BudgetExceeded(f"per-round budget ${per_round} reached for {run_id}")
        if self.spent() >= total:
            raise BudgetExceeded(f"total budget ${total} reached")

    def programme_counts(self) -> dict:
        rows = self.db.execute("SELECT programme, COUNT(*) FROM runs GROUP BY programme").fetchall()
        return {k or "?": v for k, v in rows}

    def recent_runs(self, n=10):
        return self.db.execute(
            "SELECT id,contract,programme,status,outcome FROM runs ORDER BY started DESC LIMIT ?", (n,)).fetchall()
