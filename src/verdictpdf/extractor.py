"""
Light-weight placeholder extractor for VerdictPDF
-------------------------------------------------

Keeps the public API stable (``verdictpdf.api`` expects a
``pdf_to_json`` function) while we design the full pipeline.

Current behaviour:
* opens the PDF with **pdfplumber**
* returns plain-text for every page in a JSON-ready dict
"""

from pathlib import Path
from typing import Any, Dict, List

import pdfplumber


def pdf_to_json(pdf_path: str, *, use_ocr: bool = False) -> Dict[str, Any]:
    """
    Very naïve PDF-to-JSON converter.

    Parameters
    ----------
    pdf_path : str | Path
        Path to a PDF file.
    use_ocr : bool, optional
        Placeholder flag (ignored for now).  In the real implementation
        this will trigger an OCR fallback.

    Returns
    -------
    dict
        {
            "pages": [
                {"page_num": 1, "text": "..."},
                {"page_num": 2, "text": "..."},
                ...
            ]
        }
    """
    pages: List[Dict[str, Any]] = []

    with pdfplumber.open(str(Path(pdf_path))) as pdf:
        for idx, page in enumerate(pdf.pages, start=1):
            pages.append({"page_num": idx, "text": page.extract_text() or ""})

    return {"pages": pages}