from pydantic import BaseModel
from datetime import date as date_type

from app.schemas.transaction import TransactionResponse


class ReceiptScanResponse(BaseModel):

    receipt_id: int

    merchant: str | None

    date: date_type | None

    amount: float | None

    category: str | None

    category_confidence: float | None

    raw_text: str

    saved: bool

    transaction: TransactionResponse | None
