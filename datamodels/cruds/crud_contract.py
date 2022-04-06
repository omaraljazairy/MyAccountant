from sqlalchemy.orm import Session
from datamodels import models, schema
import logging

logger = logging.getLogger('crud')


def create(db: Session, contract: schema.Contract):
    db_contract = models.Contract(
        **contract.dict()
    )
    db.add(db_contract)
    db.commit()
    db.refresh(db_contract)
    return db_contract
