import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME = "TransitOps"
    VERSION = "1.0.0"

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///./database/transit.db"
    )

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "transitops-secret-key-change-later"
    )

    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

settings = Settings()