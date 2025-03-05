from pydantic import BaseModel

###TYPES##

class TypeResponse(BaseModel):
    name: str

    class Config:
        from_attributes = True

###PACKAGES##

class PackageBase(BaseModel):
    name: str
    weight: float
    price: float
    type: TypeResponse
    delivery_price: float

    class Config:
        from_attributes = True

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