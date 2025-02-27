from pydantic import BaseModel

###PACKAGES##
class TypeResponse(BaseModel):
    name: str

    class Config:
        orm_mode = True

class PackageBase(BaseModel):
    name: str
    weight: float
    price: float
    type: TypeResponse
    delivery_price: float

    class Config:
        orm_mode = True

class Package(PackageBase):
    package_id: int

class PackageCreate(BaseModel):
    name: str
    weight: float
    price: float
    type_id: int

class PackageAfterCreate(BaseModel):
    id: int

class PackageById(PackageBase):
    ...
###TYPES##