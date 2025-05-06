from fastapi import Header, HTTPException, status, Depends
from .credits import charge

def credits_guard(
    x_api_key: str = Header(..., alias="X-API-KEY"),
    pages: int | None = None                     # filled later via dependency
) -> None:
    try:
        charge(x_api_key, pages or 0)            # 0 for validation pass
    except ValueError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid API key")