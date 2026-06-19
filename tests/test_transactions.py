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


def test_get_transactions(client: TestClient) -> None:
    client.post(
        "/transactions",
        json={
            "title": "Salary",
            "amount": 5000,
            "type": "INCOME",
            "category": "Work",
        },
    )

    response = client.get("/transactions")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1

    assert data[0]["title"] == "Salary"


def test_delete_transaction(client: TestClient) -> None:
    create_response = client.post(
        "/transactions",
        json={
            "title": "Salary",
            "amount": 5000,
            "type": "INCOME",
            "category": "Work",
        },
    )

    transaction_id = create_response.json()["id"]

    response = client.delete(f"/transactions/{transaction_id}")

    assert response.status_code == 204


def test_delete_non_existing_transaction(client: TestClient) -> None:
    response = client.delete("/transactions/999")

    assert response.status_code == 404


def test_export_transactions_csv(client: TestClient) -> None:
    client.post(
        "/transactions",
        json={
            "title": "Salary",
            "amount": 5000,
            "type": "INCOME",
            "category": "Work",
        },
    )

    response = client.get("/transactions/export/csv")

    assert response.status_code == 200

    assert (response.headers["content-type"] == "text/csv; charset=utf-8")

    assert "Salary" in response.text