import os
import uuid
from datetime import date

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.config import settings
from app.models.receipt import Receipt
from app.models.transaction import Transaction
from app.repositories.receipt_repository import ReceiptRepository
from app.ml.ocr_service import extract_text, parse_receipt
from app.ml.category_classifier import category_classifier

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp", "image/jpg"}
MAX_FILE_SIZE_BYTES = 8 * 1024 * 1024  # 8 MB


class ReceiptService:

    @staticmethod
    def _save_image(user_id: int, filename: str, content: bytes) -> str:

        extension = os.path.splitext(filename or "")[1].lower() or ".jpg"

        user_dir = os.path.join(settings.RECEIPT_STORAGE_DIR, str(user_id))
        os.makedirs(user_dir, exist_ok=True)

        stored_name = f"{uuid.uuid4().hex}{extension}"
        full_path = os.path.join(user_dir, stored_name)

        with open(full_path, "wb") as f:
            f.write(content)

        return full_path

    @staticmethod
    def scan_receipt(
        db: Session,
        user_id: int,
        file: UploadFile,
        auto_save: bool
    ) -> dict:

        if file.content_type not in ALLOWED_CONTENT_TYPES:
            raise HTTPException(
                status_code=415,
                detail=(
                    f"Unsupported file type '{file.content_type}'. "
                    f"Upload a JPEG, PNG, or WEBP image."
                )
            )

        content = file.file.read()

        if not content:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")

        if len(content) > MAX_FILE_SIZE_BYTES:
            raise HTTPException(
                status_code=413,
                detail="Image too large — max 8 MB"
            )

        try:
            raw_text = extract_text(content)
        except Exception:
            raise HTTPException(
                status_code=422,
                detail="Could not read this image — make sure it's a valid, unobstructed photo of a receipt"
            )

        parsed = parse_receipt(raw_text)

        category_result = None

        if parsed["merchant"]:
            category_result = category_classifier.predict(parsed["merchant"])

        image_path = ReceiptService._save_image(user_id, file.filename, content)

        transaction = None

        if auto_save and parsed["amount"]:

            transaction = Transaction(
                date=parsed["date"] or date.today(),
                description=parsed["merchant"] or "Receipt scan",
                amount=parsed["amount"],
                type="expense",
                category=(category_result["category"] if category_result else "Others"),
                notes="Auto-created from OCR receipt scan",
                user_id=user_id
            )

            db.add(transaction)
            db.flush()  # assign transaction.id without committing yet

        receipt = Receipt(
            user_id=user_id,
            transaction_id=transaction.id if transaction else None,
            image_path=image_path,
            raw_text=raw_text,
            parsed_merchant=parsed["merchant"],
            parsed_amount=parsed["amount"],
            parsed_date=parsed["date"]
        )

        db.add(receipt)
        db.commit()
        db.refresh(receipt)

        if transaction:
            db.refresh(transaction)

        return {
            "receipt_id": receipt.id,
            "merchant": parsed["merchant"],
            "date": parsed["date"],
            "amount": parsed["amount"],
            "category": category_result["category"] if category_result else None,
            "category_confidence": category_result["confidence"] if category_result else None,
            "raw_text": raw_text,
            "saved": transaction is not None,
            "transaction": transaction,
        }
