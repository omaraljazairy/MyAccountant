from datamodels import models
import logging

logger = logging.getLogger('fixtures')


def test_fixture_customer(db, create_customers):

    create_customers
    customer = db.query(models.Customer).all()
    logger.debug(f'customer : {customer} - {len(customer)}')

    assert len(customer) == 4


def test_fixture_contract(create_contract, db):

    create_contract
    contract = db.query(models.Contract).all()
    logger.debug(f'contract : {contract} - {len(contract)}')

    assert len(contract) == 3


def test_fixture_income(db, create_income):

    create_income
    income = db.query(models.Income).all()
    income_1 = income[0]
    logger.debug(f'income : {income} - {len(income)}')
    logger.debug(f'income_1 : {income_1} - {income_1.customer_name}')

    assert len(income) == 3
    assert income_1.customer_name == 'Bar'


def test_user_auth(auth_user):
    """ test if the user has a token."""

    token = auth_user
    logger.debug(f"token => {token}")

    assert type(token) == str
