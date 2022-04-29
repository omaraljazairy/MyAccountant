from sqlalchemy.orm import Session
from datamodels import models
from datamodels.schemas import schema_income
from datetime import date
import logging

logger = logging.getLogger('crud')


def create(db: Session, income: schema_income.Income):
    db_income = models.Income(
        **income.dict()
    )
    db.add(db_income)
    db.commit()
    db.refresh(db_income)
    return db_income

def get_all_income(db: Session):
    """return all data from the income model."""

    return db.query(models.Income).all()


def get_income_by_date(db: Session, start_date:date, end_date:date = None):
    """filter the data by start_date with an option to provide the end_date."""

    current_date = end_date if end_date else date.today() #.strftime("%Y/%m/%d")

    logger.debug(f"current_date received: {current_date}")

    return db.query(models.Income).\
        filter(models.Income.invoice_date >= start_date).\
        filter(models.Income.invoice_date < current_date).all()
    
def get_income_by_customer(db: Session, customer_id:int):
    """filter the data by customer_id."""

    logger.debug(f"customer_id: {customer_id}")

    return db.query(models.Income).join(models.Contract).\
        filter(models.Contract.customer_id == customer_id).all()
