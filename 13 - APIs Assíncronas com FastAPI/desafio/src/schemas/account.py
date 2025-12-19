from pydantic import BaseModel, PositiveFloat, Field, conint

class AccountIn(BaseModel):
    user_id: conint(gt=0) = Field(..., description="ID do usuário, deve ser maior que zero")
    balance: PositiveFloat = Field(..., description="Saldo inicial da conta, deve ser positivo")


class AccountOut(BaseModel):
    id: int = Field(..., description="ID da conta")
    user_id: int = Field(..., description="ID do usuário dono da conta")
    balance: float = Field(..., description="Saldo atual da conta")
