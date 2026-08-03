from datetime import date

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from fastapi import Response
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.security import get_current_user
from app.services.export_service import ExportService

router = APIRouter(
    tags=["Export"]
)


@router.get("/export/csv")
def export_csv(
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    content = ExportService.to_csv(db, current_user.id, date_from, date_to)

    return Response(
        content=content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=transactions.csv"}
    )


@router.get("/export/excel")
def export_excel(
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    content = ExportService.to_excel(db, current_user.id, date_from, date_to)

    return Response(
        content=content,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=transactions.xlsx"}
    )


@router.get("/export/pdf")
def export_pdf(
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    content = ExportService.to_pdf(db, current_user.id, date_from, date_to)

    return Response(
        content=content,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=transactions.pdf"}
    )
