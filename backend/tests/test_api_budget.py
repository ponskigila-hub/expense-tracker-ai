import datetime


def test_create_budget(client, auth_headers):

    r = client.post("/budget", json={"category": "Food", "amount": 100000}, headers=auth_headers)
    assert r.status_code == 201
    assert r.json()["category"] == "Food"
    assert r.json()["spent"] == 0


def test_duplicate_category_rejected(client, auth_headers):

    client.post("/budget", json={"category": "Food", "amount": 100000}, headers=auth_headers)
    r = client.post("/budget", json={"category": "Food", "amount": 200000}, headers=auth_headers)
    assert r.status_code == 409


def test_budget_warning_appears_when_close_to_limit(client, auth_headers):

    client.post("/budget", json={"category": "Food", "amount": 100000}, headers=auth_headers)

    client.post("/transactions", json={
        "date": str(datetime.date.today()), "description": "Big spend",
        "amount": 90000, "type": "expense", "category": "Food"
    }, headers=auth_headers)

    r = client.get("/budget", headers=auth_headers)
    budget = r.json()[0]
    assert budget["warning"] is not None
    assert budget["is_exceeded"] is False


def test_update_and_delete_budget(client, auth_headers):

    created = client.post("/budget", json={"category": "Food", "amount": 100000}, headers=auth_headers).json()

    updated = client.put(f"/budget/{created['id']}", json={"amount": 500000}, headers=auth_headers)
    assert updated.status_code == 200
    assert updated.json()["amount"] == 500000

    deleted = client.delete(f"/budget/{created['id']}", headers=auth_headers)
    assert deleted.status_code == 200

    r = client.put(f"/budget/{created['id']}", json={"amount": 1}, headers=auth_headers)
    assert r.status_code == 404


def test_budgets_are_isolated_per_user(client, make_user):

    _, alice = make_user("alice_budget")
    _, bob = make_user("bob_budget")

    client.post("/budget", json={"category": "Food", "amount": 100000}, headers=alice)

    r = client.get("/budget", headers=bob)
    assert r.json() == []


def test_invalid_amount_rejected(client, auth_headers):

    r = client.post("/budget", json={"category": "Food", "amount": -100}, headers=auth_headers)
    assert r.status_code == 422
