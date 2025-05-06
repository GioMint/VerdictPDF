from __future__ import annotations

import json
import os

from fastapi.testclient import TestClient
from verdictpdf.api import app

client = TestClient(app)


def test_convert_bad_token():
    r = client.post(
        "/convert",
        headers={"X-API-KEY": "NOPE"},
        files={"file": ("x.pdf", b"%PDF-1.4\n%%EOF", "application/pdf")},
    )
    assert r.status_code == 401


def test_convert_good_token(tmp_path):
    # --- create 1-page dummy PDF ---------------------------------------------
    pdf = tmp_path / "1p.pdf"
    pdf.write_bytes(b"%PDF-1.4\n%%EOF")  # minimal shell is OK for the stub

    # --- seed credits ---------------------------------------------------------
    credits = {"GOOD": 3}
    (tmp_path / "credits.json").write_text(json.dumps(credits))

    # point the service to the temp credits file
    os_environ_backup = dict(os.environ)

    os.environ["CREDITS_FILE"] = str(tmp_path / "credits.json")

    # -------------------------------------------------------------------------
    try:
        r = client.post(
            "/convert",
            headers={"X-API-KEY": "GOOD"},
            files={"file": ("x.pdf", pdf.read_bytes(), "application/pdf")},
        )
        assert r.status_code == 200
        assert r.json()["pages"][0]["page_num"] == 1

        # balance should be 2 now
        new_bal = json.loads((tmp_path / "credits.json").read_text())["GOOD"]
        assert new_bal == 2
    finally:
        # restore env to avoid side-effects for other tests
        os.environ.clear()
        os.environ.update(os_environ_backup)