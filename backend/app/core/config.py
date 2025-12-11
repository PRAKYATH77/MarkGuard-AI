import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "MarkGuard AI"
    USE_MOCK_AI: bool = str(os.getenv("USE_MOCK_AI", "False")).lower() == "true"

settings = Settings()
