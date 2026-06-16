from fastapi.testclient import TestClient


def test_create_income_transaction(client: TestClient) -> None:
    response = client.post(
        "/transactions",
        json={
            "title": "Salary",
            "amount": 5000,
            "type": "INCOME",
            "category": "Work",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Salary"
    assert data["amount"] == 5000
    assert data["type"] == "INCOME"
    assert data["category"] == "Work"


def test_create_transaction_validation_error(client: TestClient) -> None:
    response = client.post(
        "/transactions",
        json={
            "title": "",
            "amount": -100,
            "type": "INCOME",
            "category": "",
        },
    )

    assert response.status_code == 422