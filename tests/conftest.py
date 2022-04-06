import logging

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists

from app.enums import Unit
from app.main import app
from datamodels import schema
from datamodels.cruds import crud_contract, crud_customer, crud_income
from services.database import Base, get_db

logger = logging.getLogger('fixtures')

# DB
TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_test_app.db"


@pytest.fixture(scope="session")
def db_engine():
    """create the database and return an instance of the engine."""

    engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL, connect_args={
        "check_same_thread": False
        }
    )
    if not database_exists:
        create_database(engine.url)

    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(scope="session")
def db(db_engine):
    """setup the database connection and use the db_engine to use the test
    database. return a session to be available for all tests.
    """

    connection = db_engine.connect()

    # begin a non-ORM transaction
    connection.begin()

    # bind an individual Session to the connection
    db = Session(bind=connection)
    # db = Session(db_engine)

    yield db

    db.rollback()
    connection.close()


# override the get_db to use the test db during the test session
app.dependency_overrides[get_db] = lambda: db


@pytest.fixture(scope="session")
def client(db):
    """create the test client using the test database to be available for
    all tests.
    """
    app.dependency_overrides[get_db] = lambda: db

    with TestClient(app) as c:
        yield c


# DB fixtures ###
@pytest.fixture(scope="session")
def create_customers(db):

    session = db

    logger.debug('fixture started')
    crud_customer.create(session, schema.CustomerBase(name='Bar'))
    crud_customer.create(session, schema.CustomerBase(name='Bar2'))
    crud_customer.create(session, schema.CustomerBase(name='Bar3'))
    result = crud_customer.create(
        session,
        schema.CustomerBase(name='FooBar3')
        )
    logger.debug(f'fixture result from customer3 => {result.id}')


@pytest.fixture(scope="session")
def create_contract(db):

    session = db

    logger.debug('fixture started')
    crud_contract.create(session, schema.ContractBase(
        customer_id=1,
        rate=20,
        unit=Unit.HOUR.value,
        start_date='2010-01-01'
    ))

    crud_contract.create(session, schema.ContractBase(
        customer_id=2,
        rate=10,
        unit=Unit.HOUR.value,
        start_date='2010-03-01'
    ))

    result = crud_contract.create(session, schema.ContractBase(
        customer_id=3,
        rate=30,
        unit=Unit.DAY.value,
        start_date='2010-08-01'
    ))

    logger.debug(f'fixture result from contract 3 => {result.id}')


@pytest.fixture(scope="session")
def create_income(db):

    session = db

    logger.debug('fixture started')
    crud_income.create(session, schema.IncomeBase(
        total=1,
        invoice_date='2010-01-01',
        contract_id=1
        )
    )
    crud_income.create(session, schema.IncomeBase(
        total=2,
        invoice_date='2010-02-01',
        contract_id=2
        )
    )
    result = crud_income.create(session, schema.IncomeBase(
        total=3,
        invoice_date='2022-03-01',
        contract_id=3,
        )
    )
    logger.debug(f'fixture result from income_3 => {result.id}')

# AUTH USER ##


@pytest.fixture(scope="session")
def auth_user(client) -> str:
    """create a user and log him in and return a token. any endpoint that
    requires the user to be authenticated, can use this token."""

    user_data = {
        "username": "omar1",
        "password": "pass123",
        "email": "foo@bar.com"
    }
    response = client.post("/user/", json=user_data)
    logger.debug(f"response user: {response}")

    response_token = client.post("/auth/login", json={
        "username": "omar1",
        "password": "pass123"
        }
    )
    logger.debug(f"response token : {response_token.content}")

    token = response_token.json()['access_token']
    logger.debug(f"token : {token}")

    yield token
