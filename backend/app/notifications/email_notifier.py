import logging
import smtplib
from email.mime.text import MIMEText

from app.config import settings
from app.notifications.base import Notifier

logger = logging.getLogger("expense_tracker.notifications")


class EmailNotifier(Notifier):

    name = "email"

    def is_configured(self) -> bool:
        return bool(
            settings.SMTP_HOST and settings.SMTP_USER and settings.SMTP_PASSWORD
        )

    def send(self, subject: str, message: str, to_email: str | None = None) -> bool:

        if not self.is_configured():
            return False

        recipient = to_email or settings.SMTP_FROM_EMAIL

        if not recipient:
            return False

        try:
            msg = MIMEText(message)
            msg["Subject"] = subject
            msg["From"] = settings.SMTP_FROM_EMAIL
            msg["To"] = recipient

            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)

            return True

        except Exception as e:
            logger.warning(f"Email notification failed: {e}")
            return False
