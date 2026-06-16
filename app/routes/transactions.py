from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.enums import TransactionType
from app.schemas.summary import BalanceResponse, MonthlySummaryResponse
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.services.transaction_service import TransactionService

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)

@router.post(
    "",
    response_model=TransactionResponse,
    status_code=201,
    summary="Create transaction",
    tags=["Transactions"]
)
async def create_transaction(payload: TransactionCreate, db: Session = Depends(get_db)) -> TransactionResponse:
    service = TransactionService(db)

    transaction = service.create_transaction(payload)

    return TransactionResponse.model_validate(transaction)


@router.get(
    "",
    response_model=list[TransactionResponse],
    summary="Get transactions",
    tags=["Transactions"]
)
async def get_transactions(db: Session = Depends(get_db)) -> list[TransactionResponse]:
    service = TransactionService(db)

    transactions = service.get_transaction()

    return [
        TransactionResponse.model_validate(transaction)
        for transaction in transactions
    ]


@router.delete(
    "/{transaction_id}",
    status_code=204,
    summary="Delete transaction",
    tags=["Transactions"]
)
async def delete_transaction(transaction_id: int, db: Session = Depends(get_db)) -> None:
    service = TransactionService(db)

    deleted = service.delete_transaction(transaction_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found."
        )


@router.get(
    "/balance",
    response_model=BalanceResponse
)
async def get_balance(db: Session = Depends(get_db)) -> BalanceResponse:
    service = TransactionService(db)

    return service.get_balance()


@router.get(
    "/type/{transaction_type}",
    response_model=list[TransactionResponse]
)
async def get_transactions_by_type(transaction_type: TransactionType, db: Session = Depends(get_db)) -> list[[TransactionResponse]]:
    service = TransactionService(db)

    transactions = service.get_transactions_by_type(transaction_type)

    return [
        TransactionResponse.model_validate(transaction)
        for transaction in transactions
    ]


@router.get(
    "/category/{category}",
    response_model=list[TransactionResponse]
)
async def get_transactions_by_category(category: str, db: Session = Depends(get_db)) -> list[TransactionResponse]:
    service = TransactionService(db)

    transactions = service.get_transactions_by_category(category)

    return [
        TransactionResponse.model_validate(transaction)
        for transaction in transactions
    ]


@router.get(
    "/summary/{year}/{month}",
    response_model=MonthlySummaryResponse
)
async def get_monthly_summary(year: int, month: int, db: Session = Depends(get_db)) -> MonthlySummaryResponse:
    service = TransactionService(db)

    return service.get_monthly_summary(month=month, year=year)