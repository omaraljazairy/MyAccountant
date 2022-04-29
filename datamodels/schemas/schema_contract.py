from typing import List, Optional
from pydantic import BaseModel, Field
from app.enums import Unit
from datetime import date, datetime


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
        description="has to be either `day` or `hour`",
    )
    start_date: date = Field(
        title="the start date of the contract",
        description="format should be yyyy-mm-dd",
    )


class ContractUpdate(BaseModel):
    """ Only for updating a Contract """
    # id: int
    customer_id: Optional[int] = None
    rate: Optional[float] = None
    unit: Optional[Unit] = None
    start_date: Optional[date] = None


class ContractResponse(BaseModel):
    """ Represent the Contract """
    id: int
    customer_id: int
    rate: float
    unit: Unit
    start_date: date
    created: datetime

    class Config:
        orm_mode = True


class ContractCustomer(BaseModel):
    """use for the response of the creation."""
    id: int
    name: str

    class Config:
        orm_mode = True


class ContractIncome(BaseModel):
    id: int
    total: float
    invoice_month_year:str
    total_rate_excl_vat:float
    total_rate_incl_vat: float
    total_yearly_vat: float
    total_netto:float    

    class Config:
        orm_mode = True


class ContractDetails(BaseModel):
    """ Represent the Contract Details """
    id: int
    rate: float
    unit: Unit
    start_date: date
    customer: ContractCustomer
    income: List[ContractIncome]
    created: datetime

    class Config:
        orm_mode = True

