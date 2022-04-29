import logging
from fastapi import FastAPI, Depends, HTTPException
from app.config import get_settings, Settings
from services.database import engine
from datamodels import models
from routers import auth, contract, user, income, customer
import logging.config
from app.log import LOGGING


logging.config.dictConfig(LOGGING)


models.Base.metadata.create_all(bind=engine)
logger = logging.getLogger('main')

app = FastAPI()
app.include_router(router=auth.router)
app.include_router(router=user.router)
app.include_router(router=income.router)
app.include_router(router=customer.router)
app.include_router(router=contract.router)

logger.debug('main initialized')

@app.get("/")
async def first(
    settings: Settings = Depends(get_settings)
    # ,current_user: Login = Depends(auth.get_current_user)
    ):
    return {
        "foo": "bar",
        "environment": settings.environment,
        "testing": settings.testing
    }


    """
    python -m venv venv
    source venv/bin/activate
    """