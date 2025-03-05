from typing import Union

from fastapi import HTTPException
from pydantic import BaseModel, field_validator, model_validator


###TYPES##

class TypeResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

###PACKAGES##

class PackageBase(BaseModel):
    name: str
    weight: float
    price: float
    type: TypeResponse
    delivery_price: Union[float, str]

    @model_validator(mode='before')
    def check_delivery_price(cls, values):
        if not values.delivery_price:
            values.delivery_price = 'Не рассчитано'
        return values

    class Config:
        from_attributes = True

class Package(PackageBase):
    package_id: int

class PackageCreate(BaseModel):
    name: str
    weight: float
    price: float
    type_id: int

    @field_validator('price')
    def validate_price(cls, value):
        if value <= 0:
            raise HTTPException(
                status_code=422, detail="Price must be greater than 0"
            )
        return value

    @field_validator('weight')
    def validate_weight(cls, value):
        if value <= 0:
            raise HTTPException(
                status_code=422, detail="Weight must be greater than 0"
            )
        return value

class PackageAfterCreate(BaseModel):
    id: int

class PackageById(PackageBase):
    ...