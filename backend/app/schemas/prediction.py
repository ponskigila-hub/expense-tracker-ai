from pydantic import BaseModel, Field


class CategoryPredictionRequest(BaseModel):

    description: str = Field(min_length=1, max_length=200)


class CategoryPredictionResponse(BaseModel):

    description: str

    category: str

    confidence: float

    method: str
