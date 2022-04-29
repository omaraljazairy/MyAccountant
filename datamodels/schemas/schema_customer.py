from typing import List
from pydantic import BaseModel, Field
from datamodels.schemas.schema_contract import ContractResponse
from app.enums import Unit
from datetime import date, datetime


class CustomerBase(BaseModel):
    """ base model used for the api."""
    name: str = Field(
        title="The companyname working for.",
        description="A unique name of the company working for"
    )
    
    class Config:
        schema_extra={
            "example" : 
                {
                    "name": "foo.com"
                }
        }

class Customer(CustomerBase):
    id: int

    class Config:
        orm_mode = True


class CustomerUpdate(BaseModel):
    """use for the update api."""
    id: int
    name: str


class CustomerResponse(BaseModel):
    """use for the response of the creation."""
    id: int
    name: str

    class Config:
        orm_mode = True


class CustomerContract(BaseModel):
    """ Represent the Contract of the customer """
    id: int
    rate: float
    unit: Unit
    start_date: date
    created: datetime

    class Config:
        orm_mode = True


class CustomerDetailResponse(BaseModel):
    """ base model for customer details. """

    id: int
    name: str
    contract: List[CustomerContract]

    class Config:
        orm_mode = True
