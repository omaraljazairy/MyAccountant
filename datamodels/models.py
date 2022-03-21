import logging
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from services.database import Base
from app.enums import TAX


logger = logging.getLogger('models')


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True)
    created = Column(DateTime, default=datetime.now())


class Customer(Base):
    __tablename__ = "Customer"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    created = Column(DateTime, default=datetime.now())

    contract = relationship("Contract", back_populates="customer")


class Contract(Base):
    __tablename__ = "Contract"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("Customer.id"))
    unit = Column(String)
    rate = Column(Float)
    start_date = Column(Date)
    created = Column(DateTime, default=datetime.now())

    customer = relationship("Customer", back_populates="contract")
    income = relationship("Income", back_populates="contract")


class Income(Base):
    __tablename__ = "Income"


    id = Column(Integer, primary_key=True, index=True)
    total = Column(Float)
    contract_id = Column(Integer, ForeignKey('Contract.id'))
    invoice_date = Column(Date)
    created = Column(DateTime, default=datetime.now())

    contract = relationship("Contract", back_populates="income")   
            

    @property
    def invoice_month_year(self)-> str:
        """convert the date object to a month_year string and return it. """
        
        return self.invoice_date.strftime("%b-%Y")


    @property
    def rate_unit(self)-> str:
        """returns the unit of the rate. """
        
        return self.contract.unit


    @property
    def customer_name(self) -> str:
        """return the customer name. """

        return self.contract.customer.name


    @property
    def customer_id(self)->str:
        """return the customer id. """

        return self.contract.customer.id


    @property
    def total_rate_excl_vat(self) -> float:
        """ returns the monthly netto rate without the vat by multiplying
        the total by neto rate."""
        
        amount = self.contract.rate * self.total

        return round(amount,2)


    @property
    def total_rate_incl_vat(self) -> float:
        """ returns the bruto hourly rate by adding the monthly tax to the 
        hourly neto rate."""
        
        total_bruto = (self.total_rate_excl_vat * (TAX.SALES.value / 100)) + self.total_rate_excl_vat
        
        return round(total_bruto,2)


    @property
    def total_yearly_vat(self)-> float:
        """ returns the total amount of the yearly tax that needs to be paid 
        the next year."""

        total = self.total_rate_excl_vat * (TAX.INCOME_DEFAULT_BOX.value / 100)
        
        return round(total,2)

   
    @property
    def total_netto(self) -> float:
        """ returns the total amount after extracting the monthly and yearly 
        tax from it. """

        total = self.total_rate_excl_vat - self.total_yearly_vat
        return round(total,2)
