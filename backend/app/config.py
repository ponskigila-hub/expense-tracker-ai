from dotenv import load_dotenv
import os

load_dotenv()


class Settings:

    DATABASE_URL = os.getenv("DATABASE_URL")

    SECRET_KEY = os.getenv("SECRET_KEY")

    ALGORITHM = os.getenv("ALGORITHM")

    ACCESS_TOKEN_EXPIRE_MINUTES = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
    )

    # Optional — Sprint 18 (AI Spending Insight). If unset, the insight
    # endpoint transparently falls back to a deterministic, rule-based
    # generator, so the feature works out of the box without any API key.
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

    ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")

    # Sprint 19 — where uploaded receipt images are stored on disk.
    RECEIPT_STORAGE_DIR = os.getenv("RECEIPT_STORAGE_DIR", "storage/receipts")

    # Sprint 21 — Notifications. All optional; a channel is only used if
    # its config is present. Nothing is required for the app to run.
    SMTP_HOST = os.getenv("SMTP_HOST")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    SMTP_USER = os.getenv("SMTP_USER")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL", SMTP_USER)

    DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")


settings = Settings()