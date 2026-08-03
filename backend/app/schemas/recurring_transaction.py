from pydantic import BaseModel, Field
from datetime import date, datetime


class RecurringTransactionCreate(BaseModel):

    description: str = Field(min_length=1, max_length=200)

    amount: float = Field(gt=0)

    type: str

    category: str

    notes: str | None = None

    day_of_month: int = Field(ge=1, le=28)


class RecurringTransactionUpdate(BaseModel):

    description: str | None = Field(default=None, min_length=1, max_length=200)

    amount: float | None = Field(default=None, gt=0)

    category: str | None = None

    notes: str | None = None

    day_of_month: int | None = Field(default=None, ge=1, le=28)

    is_active: bool | None = None


class RecurringTransactionResponse(BaseModel):

    id: int

    description: str

    amount: float

    type: str

    category: str

    notes: str | None

    day_of_month: int

    is_active: bool

    last_run_date: date | None

    created_at: datetime

    model_config = {
        "from_attributes": True
    }
