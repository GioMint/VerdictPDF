# ---------- Dockerfile -------------------------------------------
    FROM python:3.11-slim

    # system packages (only tesseract needed for now)
    RUN apt-get update && apt-get install -y --no-install-recommends \
            tesseract-ocr && \
        rm -rf /var/lib/apt/lists/*
    
    # copy project & install in editable mode
    WORKDIR /app
    COPY pyproject.toml .
    COPY src ./src
    RUN pip install --no-cache-dir --upgrade pip && \
        pip install -e ".[all]"
    
    # run API on :8000
    EXPOSE 8000
    CMD ["uvicorn", "verdictpdf.api:app", "--host", "0.0.0.0", "--port", "8000"]
    # -----------------------------------------------------------------