from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class IncomeInput(BaseModel):
    amount: float
    regime: str  # "old" or "new"

class TaxOutput(BaseModel):
    tax: float

class TaxHistoryBase(BaseModel):
    year: int
    total_income: float
    tax_paid: float

class TaxHistoryCreate(TaxHistoryBase):
    pass

class TaxHistoryOut(TaxHistoryBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


