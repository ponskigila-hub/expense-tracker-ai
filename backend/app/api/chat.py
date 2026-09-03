from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.security import get_current_user

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter(
    tags=["AI"]
)


@router.post(
    "/chat",
    response_model=ChatResponse
)
def chat(
    payload: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    history = [turn.model_dump() for turn in payload.history]

    result = ChatService.get_reply(
        db,
        current_user.id,
        payload.message,
        history
    )

    return ChatResponse(
        reply=result["reply"],
        generated_by=result["generated_by"]
    )
