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


settings = Settings()