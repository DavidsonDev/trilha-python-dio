from pydantic import BaseModel, Field, conint


class LoginIn(BaseModel):
    user_id: conint(gt=0) = Field(..., description="ID do usuário, deve ser maior que zero")
