import logging
from sqlalchemy.orm import Session

from app.models.enums import TransactionType
from app.models.transaction import Transaction
from app.repositories.transaction_repository import TransactionRepository
from app.schemas.summary import BalanceResponse
from app.schemas.transaction import TransactionCreate

logger = logging.getLogger(__name__)


class TransactionService:
    def __init__(self, db: Session) -> None:
        self.repository = TransactionRepository(db)

    def create_transaction(self, payload: TransactionCreate) -> Transaction:
        logger.info(
            "Creating transaction: %s",
            payload.title
        )

        transaction = Transaction(
            title=payload.title,
            amount=payload.amount,
            type=payload.type,
            category=payload.category
        )

        return self.repository.create(transaction)

    def get_transaction(self) -> list[Transaction]:
        return self.repository.get_all()

    def delete_transaction(self, transaction_id: int) -> bool:
        logger.info(
            "Deleting transaction with id=%s",
            transaction_id
        )

        logger.warning(
            "Transaction %s not found",
            transaction_id
        )

        transaction = self.repository.get_by_id(transaction_id)

        if transaction is None:
            return False

        self.repository.delete(transaction)

        return True

    def get_balance(self) -> BalanceResponse:
        transactions = self.repository.get_all()

        total_income = sum(
            transaction.amount
            for transaction in transactions
            if transaction.type == TransactionType.INCOME
        )

        total_expense = sum(
            transaction.amount
            for transaction in transactions
            if transaction.type == TransactionType.EXPENSE
        )

        return BalanceResponse(
            total_income=total_income,
            total_expense=total_expense,
            balance=total_income - total_expense
        )

    def get_transactions_by_type(self, transaction_type: TransactionType) -> list[Transaction]:
        return self.repository.get_by_type(transaction_type)

    def get_transactions_by_category(self, category: str) -> list[Transaction]:
        return self.repository.get_by_category(category)