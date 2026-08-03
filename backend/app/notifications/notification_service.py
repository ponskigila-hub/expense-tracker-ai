import logging

from app.notifications.email_notifier import EmailNotifier
from app.notifications.discord_notifier import DiscordNotifier

logger = logging.getLogger("expense_tracker.notifications")

# WhatsApp isn't implemented: reliable delivery needs a paid provider
# (e.g. Twilio's WhatsApp Business API) and a verified sender number,
# which isn't something to wire up with a placeholder that silently
# does nothing. To add it for real: implement a WhatsAppNotifier(Notifier)
# here following the same interface as the two below, backed by your
# provider's SDK/API, then register it in `_channels`.

_channels = [
    EmailNotifier(),
    DiscordNotifier(),
]


class NotificationService:

    @staticmethod
    def send(subject: str, message: str, to_email: str | None = None) -> dict[str, bool]:
        """
        Sends `message` through every configured channel. Channels with
        no config in .env are skipped (not counted as failures). Never
        raises — a broken channel is logged and skipped.
        """

        results: dict[str, bool] = {}

        for channel in _channels:

            if not channel.is_configured():
                continue

            if isinstance(channel, EmailNotifier):
                results[channel.name] = channel.send(subject, message, to_email)
            else:
                results[channel.name] = channel.send(subject, message)

        if not results:
            logger.info(
                "No notification channel configured (SMTP_* / DISCORD_WEBHOOK_URL) — "
                f"skipped notification: {subject}"
            )

        return results

    @staticmethod
    def configured_channels() -> list[str]:
        return [c.name for c in _channels if c.is_configured()]
