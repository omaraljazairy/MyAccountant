from typing import List
from sqlalchemy.orm import Session
from datamodels import models
from datamodels.schemas import schema_contract
import logging

logger = logging.getLogger('crud')


def create(db: Session, contract: schema_contract.ContractBase) -> models.Contract:
    """take a contractschema object and creates a contract object.
    The created contract object will be returned."""
    db_contract = models.Contract(
        **contract.dict()
    )
    db.add(db_contract)
    db.commit()
    db.refresh(db_contract)
    return db_contract


def update(db: Session, contract: schema_contract.ContractUpdate, id: int) -> models.Contract:
    """take a contract object and the id of the contract and updates the contract
    model with it. It will return the updated contract model. 
    """

    logger.debug(f"contract received: {contract}")
    db_contract = db.query(models.Contract).get(id)
    requested_contract = contract.dict(exclude_unset=True)
    for key, value in requested_contract.items():
        setattr(db_contract, key, value)
    db.add(db_contract)
    db.commit()
    db.refresh(db_contract)
    return db_contract


def delete(db: Session, contract_id: int) -> None:
    """take the contract_id and and deletes it if found. """
    db_contract = db.query(models.Contract).get(contract_id)
    db.delete(db_contract)
    db.commit()


def fetch_all(db: Session) -> List[models.Contract]:
    """ takes no params and returns all contracts. """
    contracts = db.query(models.Contract).all()
    return contracts


def fetch_by_id(contract_id: int, db: Session) -> schema_contract.ContractDetails:
    """ takes the contract id as param and returns all data. """
    contract = db.query(models.Contract).get(contract_id)
    return contract
