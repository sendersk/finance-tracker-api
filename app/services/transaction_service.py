from sqlalchemy.orm import Session
from unicodedata import category

from app.models.transaction import Transaction
from app.repositories.transaction_repository import TransactionRepository
from app.schemas.transaction import TransactionCreate


class TransactionService:
    def __init__(self, db: Session) -> None:
        self.repository = TransactionRepository(db)

    def create_transaction(self, payload: TransactionCreate) -> Transaction:
        transaction = Transaction(
            title=payload.title,
            amount=payload.amount,
            category=payload.category
        )

        return self.repository.create(transaction)

    def get_transaction(self) -> list[Transaction]:
        return self.repository.get_all()

    def delete_transaction(self, transaction_id: int) -> bool:
        transaction = self.repository.get_by_id(transaction_id)

        if transaction is None:
            return False

        self.repository.delete(transaction)

        return True