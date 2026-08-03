from app.ml.category_classifier import category_classifier


def test_predicts_known_merchant_correctly():
    result = category_classifier.predict("McDonald's")
    assert result["category"] == "Food"


def test_predicts_bills_for_electricity():
    result = category_classifier.predict("Bayar listrik PLN")
    assert result["category"] == "Bills"


def test_predicts_income_for_salary():
    result = category_classifier.predict("Gaji bulan ini")
    assert result["category"] == "Income"


def test_gibberish_falls_back_to_others():
    result = category_classifier.predict("xyzxyz qwerty asdfgh unknown123")
    assert result["category"] == "Others"
    assert result["method"] == "default"


def test_empty_string_returns_default():
    result = category_classifier.predict("")
    assert result["category"] == "Others"
    assert result["confidence"] == 0.0


def test_confidence_is_between_0_and_1():
    result = category_classifier.predict("Steam game")
    assert 0.0 <= result["confidence"] <= 1.0
