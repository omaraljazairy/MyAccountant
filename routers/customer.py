from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from datamodels.schema import Customer, CustomerBase
from datamodels import crud, models, schema
from sqlalchemy.orm import Session
from app.config import get_settings, Settings
# from sqlalchemy.sql.functions import current_user
from services.database import get_db
from routers import auth
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


@router.get("/all", response_model=List[Customer])
async def get_all_customers(
    settings: Settings = Depends(get_settings),
    db: Session = Depends(get_db),
    current_user: schema.Login = Depends(auth.get_current_user)
    ):
    
    return crud.get_all_customers(db=db)


@router.get("/{id}", response_model=schema.CustomerDetailResponse)
async def get_all_customers(
    id: int,
    settings: Settings = Depends(get_settings),
    db: Session = Depends(get_db),
    current_user: schema.Login = Depends(auth.get_current_user)
    ):
    
    return crud.get_customer_by_id(db=db, id=id)
