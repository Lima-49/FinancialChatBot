from pydantic import BaseModel
from typing import Optional

class ConfigBancos(BaseModel):
    id_banco: Optional[int] = None
    nome_banco: str
    valor_em_conta: float


class ConfigBancosResponse(BaseModel):
    success: bool
    message: str