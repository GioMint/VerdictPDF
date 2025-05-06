"""
Minimal placeholder for token validation.

* Accept the hard-coded key  DEV-KEY  (so the demo still works)
* Everything else is rejected ⇒ caller gets 401
"""
from fastapi import Header, HTTPException, status

def credits_guard(
    x_api_key: str = Header(..., alias="X-API-KEY")   # ← match the header
) -> None:
    """Reject any key except the built-in DEV-KEY (demo only)."""
    if x_api_key != "DEV-KEY":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )