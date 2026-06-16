from fastapi.testclient import TestClient

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


def test_balance_calculation(
    db_session
) -> None:
    income = Transaction(
        title="Salary",
        amount=5000,
        type=TransactionType.INCOME,
        category="Work"
    )

    expense = Transaction(
        title="Rent",
        amount=2000,
        type=TransactionType.EXPENSE,
        category="Housing"
    )

    db_session.add(income)
    db_session.add(expense)

    db_session.commit()

    service = TransactionService(
        db_session
    )

    result = service.get_balance()

    assert result.total_income == 5000
    assert result.total_expense == 2000
    assert result.balance == 3000


def test_balance_endpoint(client: TestClient) -> None:
    client.post(
        "/transactions",
        json={
            "title": "Salary",
            "amount": 5000,
            "type": "INCOME",
            "category": "Work",
        },
    )

    client.post(
        "/transactions",
        json={
            "title": "Rent",
            "amount": 2000,
            "type": "EXPENSE",
            "category": "Housing",
        },
    )

    response = client.get("/transactions/balance")

    assert response.status_code == 200

    data = response.json()

    assert data["total_income"] == 5000
    assert data["total_expense"] == 2000
    assert data["balance"] == 3000