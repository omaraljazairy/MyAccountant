from fastapi import APIRouter, Depends, status, HTTPException
from datamodels.schema import Contract, ContractBase
from datamodels import crud, models
from sqlalchemy.orm import Session
# from sqlalchemy.sql.functions import current_user
from services.database import get_db
# from routers import auth
import logging


logger = logging.getLogger('router')
router = APIRouter(prefix='/contract', tags=['contract'])


@router.post("/", response_model=Contract)
async def add_customer(contract: ContractBase, db: Session = Depends(get_db)):
    existing_customer = db.query(models.Customer).filter(models.Customer.id == contract.customer_id).first()
    logger.info(f"existing_customer => {existing_customer}")
    if not existing_customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer does not exist"
        )
    return crud.create_contract(db=db, contract=contract)
