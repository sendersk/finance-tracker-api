from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.transaction import Transaction


class TransactionRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, transaction: Transaction) -> Transaction:
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)

        return transaction

    def get_all(self) -> list[Transaction]:
        statement = select(Transaction)

        result = self.db.execute(statement)

        return list(result.scalars().all())

    def delete(self, transaction: Transaction) -> None:
        self.db.delete(transaction)
        self.db.commit()

    def get_by_id(self, transaction_id: int) -> Transaction | None:
        statement = select(Transaction).where(Transaction.id == transaction_id)

        result = self.db.execute(statement)

        return result.scalar_one_or_none()