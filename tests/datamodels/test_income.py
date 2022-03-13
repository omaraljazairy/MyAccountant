# from fastapi.testclient import TestClient
import unittest
# from app.main import app
from datetime import date
from datamodels.models import Income, Customer, Contract
import logging
    

class DataModelsTest(unittest.TestCase):
    
    def setUp(self):
        """ setup data before tests. """

        self.logger = logging.getLogger('test')
        self.logger.info("Setup %s ", self.__class__.__name__)
        self.customer_1 = Customer(
            name='kpn'
        )
        self.customer_2 = Customer(
            name='telindus'
        )
        
        self.contract_1 = Contract(
            customer_id = self.customer_1.id,
            unit = 'hour',
            rate = 15.00,
            start_date = '2010-01-11'
        )

        self.contract_2 = Contract(
            customer_id = self.customer_2.id,
            unit = 'day',
            rate = 100.00,
            start_date = '2010-03-11'
        )


    def test_month_year(self):
        """ create an income object and expect the date of month and year to be Jun-2022."""

        income = Income(
            total = 5,
            invoice_date = date(year=2022, month=6, day= 1),
            contract_id = self.contract_1.id
        )

        month_year = income.invoice_month_year
        
        self.logger.debug(f"income month_year: {month_year}")
        
        self.assertEqual(month_year, 'Jun-2022')


    def tearDown(self):
        """ teardown all setup. """

        self.logger.info("TearDown %s", self.__class__.__name__)

