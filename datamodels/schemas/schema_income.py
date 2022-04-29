from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import date, datetime
from app.enums import Unit


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
