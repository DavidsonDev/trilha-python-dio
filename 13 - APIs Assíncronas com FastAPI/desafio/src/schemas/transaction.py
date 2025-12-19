from enum import Enum
from pydantic import BaseModel, PositiveFloat, Field, conint


class TransactionType(str, Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"


class TransactionIn(BaseModel):
    account_id: conint(gt=0) = Field(..., description="ID da conta, deve ser maior que zero")
    type: TransactionType = Field(..., description="Tipo de transação: deposit ou withdrawal")
    amount: PositiveFloat = Field(..., description="Valor da transação, deve ser positivo")

    class Config:
        use_enum_values = True


class TransactionOut(BaseModel):
    id: int = Field(..., description="ID da transação")
    account_id: int = Field(..., description="ID da conta relacionada")
    type: TransactionType = Field(..., description="Tipo de transação")
    amount: float = Field(..., description="Valor da transação")
    timestamp: str = Field(..., description="Data e hora da transação")
