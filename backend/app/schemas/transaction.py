from pydantic import BaseModel
from datetime import date
from datetime import datetime

class TransactionResponse(BaseModel):

    id: int

    date: date

    description: str

    amount: float

    type: str

    category: str

    notes: str | None

    user_id: int

    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class TransactionCreate(BaseModel):

    date: date

    description: str

    amount: float

    type: str

    category: str

    notes: str | None = None


class PaginatedTransactionResponse(BaseModel):

    items: list[TransactionResponse]

    total: int

    page: int

    page_size: int

    total_pages: int