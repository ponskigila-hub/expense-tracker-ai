from pydantic import BaseModel, Field
from datetime import datetime


class BudgetCreate(BaseModel):

    category: str = Field(min_length=1, max_length=50)

    amount: float = Field(gt=0)


class BudgetUpdate(BaseModel):

    amount: float = Field(gt=0)


class BudgetResponse(BaseModel):

    id: int

    category: str

    amount: float

    spent: float

    remaining: float

    percentage_used: float

    is_exceeded: bool

    warning: str | None

    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
