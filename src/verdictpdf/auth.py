"""
Minimal placeholder for token validation.

* Accept the hard-coded key  DEV-KEY  (so the demo still works)
* Everything else is rejected ⇒ caller gets 401
"""
from fastapi import HTTPException, status

def credits_guard(api_key: str) -> None:
    if api_key != "DEV-KEY":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid API key")
