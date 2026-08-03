import logging

from apscheduler.schedulers.background import BackgroundScheduler

from app.database.database import SessionLocal
from app.services.recurring_transaction_service import RecurringTransactionService
from app.services.budget_service import BudgetService

logger = logging.getLogger("expense_tracker.scheduler")

scheduler = BackgroundScheduler()


def run_daily_job():

    db = SessionLocal()

    try:
        created = RecurringTransactionService.generate_due_for_all_users(db)
        logger.info(f"Recurring transaction job: generated {len(created)} transaction(s)")

        alerts = BudgetService.check_and_send_alerts(db)
        logger.info(f"Budget alert job: sent {len(alerts)} alert(s)")
    finally:
        db.close()


def start_scheduler():

    # Runs once a day. Since generation is idempotent per calendar month
    # (see RecurringTransactionService._is_due), missing the exact hour
    # or the process restarting mid-day never causes duplicates.
    scheduler.add_job(
        run_daily_job,
        "interval",
        hours=24,
        id="daily_job",
        replace_existing=True
    )

    scheduler.start()


def shutdown_scheduler():
    scheduler.shutdown(wait=False)
