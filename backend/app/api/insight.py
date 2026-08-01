from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.security import get_current_user

from app.schemas.insight import InsightResponse
from app.services.insight_service import InsightService

router = APIRouter(
    tags=["AI"]
)


@router.get(
    "/insights",
    response_model=InsightResponse
)
def get_insights(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    result = InsightService.get_insights(db, current_user.id)

    return InsightResponse(
        insights=result["insights"],
        generated_by=result["generated_by"]
    )
