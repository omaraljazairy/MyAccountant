from typing import Optional, List
from pydantic import BaseModel
from datetime import date, datetime
from app.enums import Unit
from sqlalchemy.sql.sqltypes import Float


## Auth login
class Login(BaseModel):
    username: str
    password: str


## User
class UserBase(BaseModel):
    username: str
    password: str
    email: str


class CreateUser(UserBase):
    created: date


## Token
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


## CustomerBase
class ContractBase(BaseModel):
    """ represent what is required for the contract api and will be inhereted by the
    base class.
    """

    customer_id: int
    rate: float
    unit: str
    start_date: date

    class Config:
        schema_extra={
            "example": {
                "customer_id": 1,
                "rate": 10.00,
                "unit": "hour",
                "start_date": '2021-01-01'
            }
        }


class Contract(ContractBase):
    """ the model that represents the customerrate table. """
    id: int
    created: datetime

    class Config:
        orm_mode = True


## Customer
class CustomerBase(BaseModel):
    """ base model used for the api."""
    name: str
    

class Customer(CustomerBase):
    id: int

    class Config:
        orm_mode = True

class CustomerDetailResponse(BaseModel):
    """ base model for customer details. """

    id: int
    name: str
    contract: List[Contract]

    class Config:
        orm_mode = True


## Income
class IncomeBase(BaseModel):
    """ what should be validated in the api. """
    total: float
    contract_id: int
    invoice_date: date


class Income(IncomeBase):
    id: int
    created: datetime
    invoice_month_year:str
    total_rate_excl_vat:float
    total_rate_incl_vat: float
    total_yearly_vat: float
    total_netto:float
    customer_name:str
    rate_unit: Unit
    

    class Config:
        orm_mode = True


class IncomeCustomResponse(BaseModel):
    """used by get by date and customer."""
    id: int
    contract_id: int
    invoice_month_year:str
    total_rate_excl_vat:float
    total_rate_incl_vat: float
    total_yearly_vat: float
    total_netto:float
    rate_unit: Unit

    class Config:
        orm_mode = True


class ResponseIncome(BaseModel):
    income: float
    tax: Optional[float] = 0.21
    # taxed_income: taxed_income(income=income)




