# --- ExpenseTrackerAI backend image ---
FROM python:3.12-slim

# System dependency: the Tesseract OCR *binary* (Sprint 19). This is
# separate from the `pytesseract` Python package in requirements.txt —
# pytesseract is just a thin wrapper that shells out to this binary, so
# without it every /receipts/scan call would fail at runtime.
RUN apt-get update \
    && apt-get install -y --no-install-recommends tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps first, separately from the app code, so Docker's
# layer cache can skip this (slow) step on every rebuild unless
# requirements.txt itself actually changed.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the application code.
COPY . .

# Where uploaded receipt images get written (Sprint 19). Created here so
# it exists even before the app's first request; the volume in
# docker-compose.yml is what actually makes it persist across restarts.
RUN mkdir -p storage/receipts

EXPOSE 8000

# Apply any pending Alembic migrations, then start the API. Runs on
# every container start — safe/idempotent since Alembic tracks which
# migrations already ran (see alembic_version table).
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
