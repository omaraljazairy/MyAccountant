import os
import logging
from pydantic import BaseSettings
from functools import lru_cache


logger = logging.getLogger('uvicorn')

class Settings(BaseSettings):
    environment: str = os.getenv("ENVIRONMENT", "dev")
    testing: bool = os.getenv("TESTING", 1)
    DATABASE_URL = os.getenv("DATABASE_URL", False)
    LOG_LEVEL = 'DEBUG' if environment == 'dev' else 'INFO'
    MONTHLY_TAX_FROM_BRUTO = 1.21 # 21% + 100%  = 1.21 # this is to get the 21% from the total bruto
    MONTHLY_TAX = 0.21
    YEARLY_TAX = 0.37

    logger.info(f"environment: {environment}")
    logger.info(f"testing: {testing}")
    logger.info(f"LOG_LEVEL: {LOG_LEVEL}")
    logger.info(f"DATABASE_URL: {DATABASE_URL}")

@lru_cache()
def get_settings() -> BaseSettings:
    # log.info("Loading config settings from the environment.....")
    return Settings()