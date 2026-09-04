from app.services.insight_service import InsightService


def test_pct_change_basic():
    assert InsightService._pct_change(100, 150) == 50.0
    assert InsightService._pct_change(100, 50) == -50.0


def test_pct_change_zero_baseline_returns_none():
    # Can't compute a meaningful percentage change from a zero baseline.
    assert InsightService._pct_change(0, 100) is None


def test_rule_based_insight_detects_increase():

    stats = {
        "current_by_category": {"Subscription": 150000},
        "previous_by_category": {"Subscription": 100000},
        "category_averages": {},
        "current_total_expense": 150000,
        "previous_total_expense": 100000,
        "current_income": 0,
        "previous_income": 0,
        "has_enough_history": True,
    }

    insights = InsightService.generate_rule_based_insights(stats)

    assert any("Subscription" in i and "increased" in i for i in insights)


def test_rule_based_insight_no_history_message(): 

    stats = {
        "current_by_category": {}, "previous_by_category": {}, "category_averages": {},
        "current_total_expense": 0, "previous_total_expense": 0,
        "current_income": 0, "previous_income": 0, "has_enough_history": False,
    }

    insights = InsightService.generate_rule_based_insights(stats)

    assert len(insights) == 1
    assert "not enough" in insights[0].lower()


def test_llm_insights_returns_none_without_api_key():

    from app.config import settings
    original = settings.GEMINI_API_KEY
    settings.GEMINI_API_KEY = None

    try:
        result = InsightService.generate_llm_insights({"this_month": "2026-08", "last_month": "2026-07",
            "current_by_category": {}, "previous_by_category": {}, "category_averages": {},
            "current_total_expense": 0, "previous_total_expense": 0,
            "current_income": 0, "previous_income": 0})
        assert result is None
    finally:
        settings.GEMINI_API_KEY = original
