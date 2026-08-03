from abc import ABC, abstractmethod


class Notifier(ABC):

    name: str = "base"

    @abstractmethod
    def is_configured(self) -> bool:
        """Whether enough config is present in .env to use this channel."""
        ...

    @abstractmethod
    def send(self, subject: str, message: str) -> bool:
        """Send a notification. Returns True on success, False on failure.
        Must never raise — failures should degrade gracefully so one
        broken channel doesn't block the others."""
        ...
