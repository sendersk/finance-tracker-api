from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class TransactionCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=100
    )

    amount: float = Field(
        gt=0
    )

    category: str = Field(
        min_length=1,
        max_length=50
    )


class TransactionResponse(BaseModel):
    id: int
    title: str
    amount: float
    category: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)