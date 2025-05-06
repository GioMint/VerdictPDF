from __future__ import annotations
import json, threading, os
from pathlib import Path
from typing import Dict

_LOCK = threading.Lock()                      # thread-safe in Uvicorn workers


def _credits_file() -> Path:
    """Return the current credits.json path (honours $CREDITS_FILE each call)."""
    return Path(os.getenv("CREDITS_FILE", "credits.json"))


def _load() -> Dict[str, int]:
    f = _credits_file()
    if not f.exists():
        return {}
    with f.open("r") as fh:
        return json.load(fh)


def _save(data: Dict[str, int]) -> None:
    f = _credits_file()
    tmp = f.with_suffix(".tmp")               # write → rename (atomic-ish)
    with tmp.open("w") as fh:
        json.dump(data, fh, indent=2)
    tmp.replace(f)


def charge(token: str, pages: int) -> None:
    """Subtract *pages* credits or raise ValueError."""
    with _LOCK:
        db = _load()
        if token not in db or db[token] < pages:
            raise ValueError("insufficient credits")
        db[token] -= pages
        _save(db)