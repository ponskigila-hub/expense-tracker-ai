from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.security import get_current_user

from app.notifications.notification_service import NotificationService
from app.services.budget_service import BudgetService

router = APIRouter(
    tags=["Notifications"]
)


@router.post("/notifications/test")
def send_test_notification(
    current_user: User = Depends(get_current_user)
):
    """
    Sends a test message through every configured channel (SMTP /
    Discord webhook), so you can confirm your .env credentials actually
    work before relying on real budget alerts.
    """

    results = NotificationService.send(
        subject="ExpenseTrackerAI test notification",
        message=f"Hi {current_user.username}, this is a test notification from ExpenseTrackerAI.",
        to_email=current_user.email
    )

    return {
        "configured_channels": NotificationService.configured_channels(),
        "sent": results
    }


@router.post("/notifications/check-budget-alerts")
def trigger_budget_alert_check(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Manually triggers the same budget-threshold check the scheduler runs
    daily (across ALL users, by design — alerts are inherently a global
    background job, not a per-user action). Exposed here so it's
    demoable/testable on demand rather than waiting for the scheduler.
    """

    return {"alerts_sent": BudgetService.check_and_send_alerts(db)}
