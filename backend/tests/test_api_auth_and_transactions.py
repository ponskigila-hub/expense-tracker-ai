import datetime


def test_register_and_login(client):

    r = client.post("/register", json={
        "username": "alice", "email": "alice@test.com", "password": "password123"
    })
    assert r.status_code == 201

    r = client.post("/login", json={"email": "alice@test.com", "password": "password123"})
    assert r.status_code == 200
    assert "access_token" in r.json()


def test_login_wrong_password_rejected(client):

    client.post("/register", json={
        "username": "bob", "email": "bob@test.com", "password": "correct-password"
    })

    r = client.post("/login", json={"email": "bob@test.com", "password": "wrong-password"})
    assert r.status_code in (401, 400)


def test_transactions_require_auth(client):
    assert client.get("/transactions").status_code == 403
    assert client.post("/transactions", json={}).status_code == 403


def test_invalid_token_rejected(client):
    r = client.get("/transactions", headers={"Authorization": "Bearer not-a-real-token"})
    assert r.status_code == 401


def test_create_and_list_transaction(client, auth_headers):

    r = client.post("/transactions", json={
        "date": str(datetime.date.today()), "description": "Coffee",
        "amount": 30000, "type": "expense", "category": "Food"
    }, headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["amount"] == 30000

    r2 = client.get("/transactions", headers=auth_headers)
    assert r2.json()["total"] == 1


def test_update_and_delete_transaction(client, auth_headers):

    created = client.post("/transactions", json={
        "date": str(datetime.date.today()), "description": "Coffee",
        "amount": 30000, "type": "expense", "category": "Food"
    }, headers=auth_headers).json()

    updated = client.put(f"/transactions/{created['id']}", json={
        "date": str(datetime.date.today()), "description": "Coffee (large)",
        "amount": 45000, "type": "expense", "category": "Food"
    }, headers=auth_headers)
    assert updated.status_code == 200
    assert updated.json()["amount"] == 45000

    deleted = client.delete(f"/transactions/{created['id']}", headers=auth_headers)
    assert deleted.status_code == 200

    fetch_after_delete = client.get(f"/transactions/{created['id']}", headers=auth_headers)
    assert fetch_after_delete.status_code == 404


def test_users_cannot_see_each_others_transactions(client, make_user):

    _, alice_headers = make_user("alice_iso")
    _, bob_headers = make_user("bob_iso")

    alice_txn = client.post("/transactions", json={
        "date": str(datetime.date.today()), "description": "Alice's secret",
        "amount": 1000, "type": "expense", "category": "Food"
    }, headers=alice_headers).json()

    # Bob's list must not contain Alice's transaction.
    bob_list = client.get("/transactions", headers=bob_headers).json()
    assert bob_list["total"] == 0

    # Bob directly requesting Alice's transaction ID gets 404, not 403 —
    # this must not leak whether the ID exists.
    r = client.get(f"/transactions/{alice_txn['id']}", headers=bob_headers)
    assert r.status_code == 404

    r = client.delete(f"/transactions/{alice_txn['id']}", headers=bob_headers)
    assert r.status_code == 404

    # Alice can still access her own.
    r = client.get(f"/transactions/{alice_txn['id']}", headers=alice_headers)
    assert r.status_code == 200
