from pydantic import BaseModel, Field
from typing import Literal


class ChatMessage(BaseModel):
    """A single turn in the conversation, as sent back by the client so
    the assistant has multi-turn context (the server itself is stateless)."""

    role: Literal["user", "assistant"]

    content: str = Field(min_length=1, max_length=2000)


class ChatRequest(BaseModel):

    message: str = Field(min_length=1, max_length=1000)

    # Prior turns, oldest first, NOT including `message` itself.
    # Capped so a long-running conversation can't blow up the prompt size.
    history: list[ChatMessage] = Field(default_factory=list, max_length=20)


class ChatResponse(BaseModel):

    reply: str

    generated_by: Literal["llm", "rule_based"]
