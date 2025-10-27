from pydantic import BaseModel
from typing import Optional

class ConfigAccountModelRequest(BaseModel):
    account_id: Optional[int] = None
    account_name: str
    account_balance: float

class ConfigAccountModelResponse(BaseModel):
    success: bool
    message: str