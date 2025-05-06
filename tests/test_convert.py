from fastapi.testclient import TestClient
from verdictpdf.api import app


client = TestClient(app)

def test_convert_bad_token():
    r = client.post("/convert", headers={"X-API-KEY": "NOPE"}, files={"file": ("x.pdf", b"%PDF-1.4")})
    assert r.status_code == 401