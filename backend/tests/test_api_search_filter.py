import datetime


def _seed(client, headers):

    today = datetime.date.today()
    items = [
        {"date": str(today), "description": "McDonald's lunch", "amount": 50000, "type": "expense", "category": "Food"},
        {"date": str(today), "description": "KFC dinner", "amount": 70000, "type": "expense", "category": "Food"},
        {"date": str(today - datetime.timedelta(days=5)), "description": "Netflix", "amount": 150000, "type": "expense", "category": "Subscription"},
        {"date": str(today - datetime.timedelta(days=10)), "description": "Salary", "amount": 5000000, "type": "income", "category": "Salary"},
    ]

    for item in items:
        assert client.post("/transactions", json=item, headers=headers).status_code == 200


def test_filter_by_category(client, auth_headers):

    _seed(client, auth_headers)

    r = client.get("/transactions?category=Food", headers=auth_headers)
    j = r.json()
    assert j["total"] == 2
    assert all(t["category"] == "Food" for t in j["items"])


def test_filter_by_type(client, auth_headers):

    _seed(client, auth_headers)

    r = client.get("/transactions?type=income", headers=auth_headers)
    assert r.json()["total"] == 1


def test_search_text(client, auth_headers):

    _seed(client, auth_headers)

    r = client.get("/transactions?search=mcdonald", headers=auth_headers)
    j = r.json()
    assert j["total"] == 1
    assert "McDonald" in j["items"][0]["description"]


def test_amount_range(client, auth_headers):

    _seed(client, auth_headers)

    r = client.get("/transactions?min_amount=60000&max_amount=200000", headers=auth_headers)
    amounts = sorted(t["amount"] for t in r.json()["items"])
    assert amounts == [70000, 150000]


def test_sorting(client, auth_headers):

    _seed(client, auth_headers)

    r = client.get("/transactions?sort_by=amount&sort_order=asc", headers=auth_headers)
    amounts = [t["amount"] for t in r.json()["items"]]
    assert amounts == sorted(amounts)


def test_pagination(client, auth_headers):

    _seed(client, auth_headers)

    p1 = client.get("/transactions?page=1&page_size=2", headers=auth_headers).json()
    p2 = client.get("/transactions?page=2&page_size=2", headers=auth_headers).json()

    assert p1["total"] == 4
    assert p1["total_pages"] == 2
    assert len(p1["items"]) == 2
    assert len(p2["items"]) == 2

    ids_p1 = {t["id"] for t in p1["items"]}
    ids_p2 = {t["id"] for t in p2["items"]}
    assert ids_p1.isdisjoint(ids_p2)  # no overlap between pages


def test_invalid_sort_by_rejected(client, auth_headers):

    r = client.get("/transactions?sort_by=not_a_real_column", headers=auth_headers)
    assert r.status_code == 422


def test_no_matches_returns_empty_not_error(client, auth_headers):

    _seed(client, auth_headers)

    r = client.get("/transactions?category=DoesNotExist", headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["total"] == 0
    assert r.json()["items"] == []
