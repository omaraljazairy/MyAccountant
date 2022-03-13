from typing import Optional
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


# class IncomeByDate(BaseModel):
#     """required for the request by invoice_date. """

#     start_date: str
#     end_date: str = None



# def taxed_income(income: Income, settings: Settings):
#     total_hours = get_total_hours(
#         hours_per_day=income.hours_per_day, 
#         days=income.days
#     )
#     bruto_income = get_total_bruto_income(total_hours=total_hours, customer_id=income.customer_id)
#     monthly_tax = bruto_income - round(bruto_income / settings.MONTHY_TAX)
#     monthly_taxed = bruto_income - monthly_tax
#     yearly_tax = round(monthly_taxed * settings.YEARLY_TAX)
#     netto_income = monthly_taxed - yearly_tax

#     total_hourly_income = Income(
#         hours_per_day=income.hours_per_day,
#         days=income.days,
#         date=income.date,
#         customer_id=income.customer_id,
#         bruto_income=bruto_income,
#         total_hours=total_hours,
#         monthly_tax=monthly_tax,
#         monthly_taxed=monthly_taxed,
#         yearly_tax=yearly_tax,
#         netto_income=netto_income
#     )
#     return total_hourly_income


# def get_total_hours(hours_per_day:int, days:int) -> int:
#     """ return the total hours. """
    
#     total_hours = hours_per_day * days
#     return total_hours

# def get_total_bruto_income(total_hours:int, customer_id:int) -> float:
#     """ returns the total bruto income based on the total hours and customer. """

#     bruto_income = total_hours * (KPN_HOURLY_RATE if customer_id == 1 else TELINDUS_HOURLY_RATE)
#     return bruto_income




class ResponseIncome(BaseModel):
    income: float
    tax: Optional[float] = 0.21
    # taxed_income: taxed_income(income=income)




