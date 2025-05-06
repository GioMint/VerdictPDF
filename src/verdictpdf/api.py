""" VerdictPDF – FastAPI entry-point
------------------------------------
(… docstring unchanged …)
"""
from __future__ import annotations

import os
import tempfile
from pathlib import Path

# ⬇️ split the long FastAPI import so we can add Header cleanly
from fastapi import (
    Depends,
    FastAPI,
    File,
    Header,              #  ← NEW
    HTTPException,
    Query,
    UploadFile,
    status,
)
from fastapi.responses import JSONResponse

from .auth import credits_guard
from . import extractor
from .credits import charge       #  ← NEW

app = FastAPI(title="VerdictPDF API")


@app.post(
    "/convert",
    dependencies=[Depends(credits_guard)],
    summary="Convert PDF → JSON",
    responses={401: {"description": "Invalid API key / no credits"}},
)
async def convert(
    file: UploadFile = File(..., description="PDF to convert"),
    ocr: bool = Query(
        False,
        description="Enable OCR fallback (costs the same number of credits)",
    ),
    x_api_key: str = Header(..., alias="X-API-KEY"),   #  ← NEW (needed by charge)
):
    # --- basic validation -----------------------------------------------------
    if file.content_type not in ("application/pdf", "application/octet-stream"):
        raise HTTPException(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "File must be a PDF"
        )

    # --- save to temp file ----------------------------------------------------
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp_path = Path(tmp.name)
        tmp.write(await file.read())
        tmp.flush()

    # --- call the extractor ---------------------------------------------------
    try:
        result = extractor.pdf_to_json(str(tmp_path), use_ocr=ocr)
        # --- deduct credits (1 page = 1 credit) -------------------------------
        charge(x_api_key, len(result["pages"]))        #  ← NEW
    finally:
        # best-effort cleanup
        try:
            os.remove(tmp_path)
        except FileNotFoundError:
            pass

    return JSONResponse(result, status_code=status.HTTP_200_OK)