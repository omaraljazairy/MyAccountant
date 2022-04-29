from sqlalchemy.orm import Session
from datamodels import models
from datamodels.schemas import schema_customer
import logging

logger = logging.getLogger('crud')

# CUSTOMER

def get_all_customers(db: Session):
    """return all data from the customer model."""

    return db.query(models.Customer).all()

def get_customer_by_id(db: Session, id: int):
    """return customer data by customer id."""

    return db.query(models.Customer).get(id)


def create(db: Session, customer: schema_customer.Customer):
    db_customer = models.Customer(
        **customer.dict()
    )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def update(db: Session, customer: schema_customer.Customer):
    db_customer = db.query(models.Customer).get(customer.id)
    db_customer.name = customer.name
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def delete(db: Session, customer_id: int ) -> None:
    db_customer = db.query(models.Customer).get(customer_id)
    db.delete(db_customer)
    db.commit()
