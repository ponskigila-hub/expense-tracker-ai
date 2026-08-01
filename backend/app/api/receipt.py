from fastapi import APIRouter
from fastapi import Depends
from fastapi import UploadFile
from fastapi import File
from fastapi import Query
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.security import get_current_user

from app.schemas.receipt import ReceiptScanResponse
from app.services.receipt_service import ReceiptService

router = APIRouter(
    tags=["AI"]
)


@router.post(
    "/receipts/scan",
    response_model=ReceiptScanResponse
)
def scan_receipt(
    file: UploadFile = File(...),
    auto_save: bool = Query(
        default=True,
        description="If true, automatically creates a transaction from the parsed total. "
                    "If false, only returns the parsed preview for the user to confirm."
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return ReceiptService.scan_receipt(
        db,
        current_user.id,
        file,
        auto_save
    )
