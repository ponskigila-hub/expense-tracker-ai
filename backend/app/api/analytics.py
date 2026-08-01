from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from typing import List
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.security import get_current_user

from app.schemas.analytics import (
    DashboardResponse,
    MonthlySummaryItem,
    CategorySummaryItem,
    TrendPoint,
    TrendPeriod,
)
from app.services.analytics_service import AnalyticsService

router = APIRouter(
    tags=["Analytics"]
)


@router.get(
    "/dashboard",
    response_model=DashboardResponse
)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return AnalyticsService.get_dashboard(db, current_user.id)


@router.get(
    "/summary/monthly",
    response_model=List[MonthlySummaryItem]
)
def get_monthly_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return AnalyticsService.get_monthly_summary(db, current_user.id)


@router.get(
    "/summary/category",
    response_model=List[CategorySummaryItem]
)
def get_category_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return AnalyticsService.get_category_summary(db, current_user.id)


@router.get(
    "/summary/trend",
    response_model=List[TrendPoint]
)
def get_trend(
    period: TrendPeriod = Query(
        default="30d",
        description="7d = last 7 days, 30d = last 30 days, 12m = last 12 months"
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return AnalyticsService.get_trend(db, current_user.id, period)
