from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.services.transaction_service import TransactionService

router = APIRouter()


@router.get("/")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/transactions", response_model=TransactionResponse, status_code=201)
async def create_transaction(payload: TransactionCreate, db: Session = Depends(get_db)) -> TransactionResponse:
    service = TransactionService(db)

    transaction = service.create_transaction(payload)

    return TransactionResponse.model_validate(transaction)