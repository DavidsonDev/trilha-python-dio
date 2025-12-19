from fastapi import APIRouter, Depends, status, HTTPException
from src.schemas.transaction import TransactionIn
from src.security import get_current_user
from src.services.transaction import TransactionService
from src.views.transaction import TransactionOut
from src.exceptions import BusinessError

router = APIRouter(prefix="/transactions")

service = TransactionService()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TransactionOut)
async def create_transaction(
    transaction: TransactionIn,
    current_user: dict = Depends(get_current_user)
):


    try:
        return await service.create(transaction, current_user["user_id"])
    except BusinessError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
