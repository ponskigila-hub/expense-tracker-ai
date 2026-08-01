from fastapi import APIRouter
from fastapi import Depends

from app.models.user import User
from app.security import get_current_user

from app.schemas.prediction import (
    CategoryPredictionRequest,
    CategoryPredictionResponse,
)
from app.ml.category_classifier import category_classifier

router = APIRouter(
    tags=["AI"]
)


@router.post(
    "/predict-category",
    response_model=CategoryPredictionResponse
)
def predict_category(
    payload: CategoryPredictionRequest,
    current_user: User = Depends(get_current_user)
):

    result = category_classifier.predict(payload.description)

    return CategoryPredictionResponse(
        description=payload.description,
        category=result["category"],
        confidence=result["confidence"],
        method=result["method"]
    )
