# src/config/settings.py

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    Central configuration loaded from environment variables.
    Works with:
    - .env (local)
    - GitHub Secrets (CI/CD)
    - Docker / Kubernetes
    """

    DB_URL = os.getenv("DB_URL")
    KAFKA_BROKER = os.getenv("KAFKA_BROKER")
    APP_ENV = os.getenv("APP_ENV", "dev")

    if not DB_URL:
        raise ValueError("DB_URL missing in environment")

    if not KAFKA_BROKER:
        raise ValueError("KAFKA_BROKER missing in environment")