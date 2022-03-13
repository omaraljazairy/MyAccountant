from fastapi import APIRouter, Depends, status, HTTPException
from datamodels.schema import Customer, CustomerBase
from datamodels import crud, models
from sqlalchemy.orm import Session
# from sqlalchemy.sql.functions import current_user
from services.database import get_db
# from routers import auth
import logging


logger = logging.getLogger('router')
router = APIRouter(prefix='/customer', tags=['customer'])


@router.post("/", response_model=Customer)
async def add_customer(customer: CustomerBase, db: Session = Depends(get_db)):
    existing_customer = db.query(models.Customer).filter(models.Customer.name == customer.name).first()
    logger.info(f"existing_customer => {existing_customer}")
    if existing_customer:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Customer {customer.name} already exists"
        )
    return crud.create_customer(db=db, customer=customer)
