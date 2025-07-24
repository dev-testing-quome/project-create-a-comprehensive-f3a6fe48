from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class User(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True

class TradeCreate(BaseModel):
    user_id: int
    symbol: str
    quantity: int
    price: float
    trade_type: str # buy or sell

class Trade(BaseModel):
    id: int
    user_id: int
    symbol: str
    quantity: int
    price: float
    trade_type: str
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True
