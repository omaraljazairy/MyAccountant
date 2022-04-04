from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import date, datetime
from app.enums import Unit



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

    customer_id: int = Field(
        title="the customer's id",
        description="the Id of the existing customer",
        )
    rate: float = Field(
        title="float number of the hourly or daily netto rate",
        description="a float number of the hourly or daily netto rate",
        gt=0
    )
    unit: Unit = Field(
        title="hour or day",
        description="has to be either `day` or `hour`"
    )
    start_date: date = Field(
        title="the start date of the contract",
        description="format should be yyyy-mm-dd"
    )

    class Config:
        schema_extra={
            "example": [
                {
                    "customer_id": 1,
                    "rate": 10.00,
                    "unit": Unit.HOUR,
                    "start_date": '2021-01-01'

                },
                {
                    "customer_id": 2,
                    "rate": 100.00,
                    "unit": Unit.DAY,
                    "start_date": '2021-05-01'

                }                
            ]
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
    name: str = Field(
        title="The companyname working for.",
        description="A unique name of the company working for"
    )
    
    class Config:
        schema_extra={
            "example" : [
                {
                    "name": "foo.com"
                },
                {
                    "name": "bar.com"
                }
            ]

        }


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
    total: float = Field(
        title="number of units",
        description="this could be the total days if the unit in the \
            contract is day or hours if unit is hour")
    contract_id: int = Field(
        title="The stored local contract_id",
        description="The contract that belongs to the income"
    )
    invoice_date: date = Field(
        title="The date of the generated invoice",
        description="the date format should be yyyy-mm-dd"
    )


    class Config:
        schema_extra={
            "example" : [
                {
                    "total": 30.5,
                    "contract_id": 1,
                    "invoice_date": "2020-04-05"
                },
                {
                    "total": 20,
                    "contract_id": 2,
                    "invoice_date": "2020-08-01"
                }
            ]

        }



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




