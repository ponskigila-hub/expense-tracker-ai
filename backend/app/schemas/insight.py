from pydantic import BaseModel
from typing import Literal


class InsightResponse(BaseModel):

    insights: list[str]

    generated_by: Literal["llm", "rule_based"]
