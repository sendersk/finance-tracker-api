import logging
from datetime import datetime, UTC
from sqlalchemy.orm import Session

from app.models.enums import TransactionType
from app.models.transaction import Transaction
from app.repositories.transaction_repository import TransactionRepository
from app.schemas.summary import BalanceResponse, MonthlySummaryResponse
from app.schemas.transaction import TransactionCreate
from app.services.export_service import ExportService

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

        logger.info("Calculating balance")

        total_income = (self.repository.get_total_amount_by_type(TransactionType.INCOME))

        total_expense = (self.repository.get_total_amount_by_type(TransactionType.EXPENSE))

        return BalanceResponse(
            total_income=total_income,
            total_expense=total_expense,
            balance=total_income - total_expense
        )

    def get_transactions_by_type(self, transaction_type: TransactionType) -> list[Transaction]:
        return self.repository.get_by_type(transaction_type)

    def get_transactions_by_category(self, category: str) -> list[Transaction]:
        return self.repository.get_by_category(category)

    def get_monthly_summary(
            self,
            month: int,
            year: int
    ) -> MonthlySummaryResponse:
        logger.info(
            "Generating monthly summary for %s-%s",
            year,
            month
        )

        start_date, end_date = self._get_month_range(
            year,
            month
        )

        total_income = (
            self.repository.get_total_amount_by_type_and_period(
                TransactionType.INCOME,
                start_date,
                end_date
            )
        )

        total_expense = (
            self.repository.get_total_amount_by_type_and_period(
                TransactionType.EXPENSE,
                start_date,
                end_date
            )
        )

        return MonthlySummaryResponse(
            month=month,
            year=year,
            total_income=total_income,
            total_expense=total_expense,
            balance=total_income - total_expense
        )

    def _get_month_range(
            self,
            year: int,
            month: int
    ) -> tuple[datetime, datetime]:
        start_date = datetime(year, month, 1, tzinfo=UTC)

        if month == 12:
            end_date = datetime(year + 1, 1, 1, tzinfo=UTC)
        else:
            end_date = datetime(year, month + 1, 1, tzinfo=UTC)

        return start_date, end_date

    def export_transactions_csv(self) -> str:
        transactions = self.repository.get_all()

        return ExportService.transactions_to_csv(transactions)