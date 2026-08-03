import logging
import httpx

from app.config import settings
from app.notifications.base import Notifier

logger = logging.getLogger("expense_tracker.notifications")


class DiscordNotifier(Notifier):

    name = "discord"

    def is_configured(self) -> bool:
        return bool(settings.DISCORD_WEBHOOK_URL)

    def send(self, subject: str, message: str) -> bool:

        if not self.is_configured():
            return False

        try:
            response = httpx.post(
                settings.DISCORD_WEBHOOK_URL,
                json={"content": f"**{subject}**\n{message}"},
                timeout=10.0
            )
            response.raise_for_status()
            return True

        except Exception as e:
            logger.warning(f"Discord notification failed: {e}")
            return False
