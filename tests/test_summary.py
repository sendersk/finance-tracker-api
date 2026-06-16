from app.models.enums import TransactionType
from app.models.transaction import Transaction
from app.services.transaction_service import TransactionService


def test_empty_balance_returns_zero(
    db_session
) -> None:
    service = TransactionService(
        db_session
    )

    result = service.get_balance()

    assert result.total_income == 0
    assert result.total_expense == 0
    assert result.balance == 0