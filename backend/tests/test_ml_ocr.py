import datetime

import pytest

from app.ml.ocr_service import normalize_amount, extract_date, extract_merchant, parse_receipt


@pytest.mark.parametrize("raw,expected", [
    ("150.000", 150000.0),
    ("Rp 150.000", 150000.0),
    ("1.234.567", 1234567.0),
    ("150,000.00", 150000.0),
    ("150.000,00", 150000.0),
    ("50000", 50000.0),
    ("12,50", 12.5),
])
def test_normalize_amount(raw, expected):
    assert normalize_amount(raw) == expected


def test_normalize_amount_garbage_returns_none():
    assert normalize_amount("no digits here") is None


@pytest.mark.parametrize("text,expected", [
    ("Tanggal: 01/08/2026", datetime.date(2026, 8, 1)),
    ("Date: 2026-08-01", datetime.date(2026, 8, 1)),
    ("1 Agustus 2026", datetime.date(2026, 8, 1)),
])
def test_extract_date(text, expected):
    assert extract_date(text) == expected


def test_extract_date_no_date_returns_none():
    assert extract_date("no date anywhere in this text") is None


def test_extract_merchant_takes_first_meaningful_line():
    text = "===================\nWARUNG BU SITI\n123456"
    assert extract_merchant(text) == "WARUNG BU SITI"


def test_parse_receipt_full_pipeline():

    sample = """
    McDonald's Sudirman
    Tanggal: 01/08/2026

    Total Bayar          82.500
    """

    result = parse_receipt(sample)

    assert result["merchant"] == "McDonald's Sudirman"
    assert result["date"] == datetime.date(2026, 8, 1)
    assert result["amount"] == 82500.0
