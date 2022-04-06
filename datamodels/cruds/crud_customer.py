from sqlalchemy.orm import Session
from datamodels import models, schema
import logging

logger = logging.getLogger('crud')

# CUSTOMER

def get_all_customers(db: Session):
    """return all data from the customer model."""

    return db.query(models.Customer).all()

def get_customer_by_id(db: Session, id: int):
    """return customer data by customer id."""

    return db.query(models.Customer).get(id)


def create(db: Session, customer: schema.Customer):
    db_customer = models.Customer(
        **customer.dict()
    )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer
