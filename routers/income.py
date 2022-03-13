from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from datamodels import schema, crud
from sqlalchemy.orm import Session
# from sqlalchemy.sql.functions import current_user
from services.database import get_db
from app.config import get_settings, Settings
from routers import auth
import logging
from datetime import date


logger = logging.getLogger('router')
router = APIRouter(prefix='/income', tags=['income'])


@router.post("/", response_model=schema.Income)
async def add_income(
    income: schema.IncomeBase, 
    settings: Settings = Depends(get_settings),
    db: Session = Depends(get_db),
    current_user: schema.Login = Depends(auth.get_current_user)
    ):
    # get the customer_rate objct
    return crud.create_income(db=db, income=income)

    # return schema.taxed_income(income=income, settings=settings)


@router.get("/all/", response_model=List[schema.IncomeCustomResponse])
async def get_all_income(
    settings: Settings = Depends(get_settings),
    db: Session = Depends(get_db),
    current_user: schema.Login = Depends(auth.get_current_user)
    ):
    
    return crud.get_all_income(db=db)


@router.get("/by_date/{start_date}/", response_model=List[schema.IncomeCustomResponse])
async def get_by_invoice_date(
    start_date:date,
    end_date: date = None,
    db: Session = Depends(get_db),
    current_user: schema.Login = Depends(auth.get_current_user)
    ):

    result = {'start_date': start_date, 'end_date': end_date }
    logger.debug(f"income params: {result}")

    return crud.get_income_by_date(db=db, start_date=start_date, end_date=end_date)


@router.get("/by_customer/{customer_id}/", response_model=List[schema.IncomeCustomResponse])
async def get_by_customer_id(
    customer_id:int,
    db: Session = Depends(get_db),
    current_user: schema.Login = Depends(auth.get_current_user)
    ):

    return crud.get_income_by_customer(db=db, customer_id=customer_id)
    