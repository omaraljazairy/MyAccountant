from sqlalchemy.orm import Session
from . import models, schema
from datetime import date
import logging

logger = logging.getLogger('crud')

# CUSTOMER

def get_all_customers(db: Session):
    """return all data from the customer model."""

    return db.query(models.Customer).all()

def get_customer_by_id(db: Session, id: int):
    """return customer data by customer id."""

    return db.query(models.Customer).get(id)


def create_customer(db: Session, customer: schema.Customer):
    db_customer = models.Customer(
        **customer.dict()
    )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


# CONTRACT

def create_contract(db: Session, contract: schema.Contract):
    db_contract = models.Contract(
        **contract.dict()
    )
    db.add(db_contract)
    db.commit()
    db.refresh(db_contract)
    return db_contract


# INCOME

def create_income(db: Session, income: schema.Income):
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
        # join(models.Contract).filter(models.Contract.customer_id == customer_id)
        # filter(models.Income.customer_name == customer_id).all()
