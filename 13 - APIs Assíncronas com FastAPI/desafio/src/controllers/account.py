from fastapi import APIRouter, Depends, status, HTTPException
from src.schemas.account import AccountIn
from src.security import get_current_user
from src.services.account import AccountService
from src.services.transaction import TransactionService
from src.views.account import AccountOut, TransactionOut
from src.exceptions import AccountNotFoundError, BusinessError

router = APIRouter(prefix="/accounts")

account_service = AccountService()
tx_service = TransactionService()


@router.get("/", response_model=list[AccountOut])
async def read_accounts(
    limit: int = 100,
    skip: int = 0,
    current_user: dict = Depends(get_current_user)
):

    return await account_service.read_all(limit=limit, skip=skip)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AccountOut)
async def create_account(
    account: AccountIn,
    current_user: dict = Depends(get_current_user)
):

    return await account_service.create(account)


@router.get("/{account_id}/transactions", response_model=list[TransactionOut])
async def read_account_transactions(
    account_id: int,
    limit: int = 100,
    skip: int = 0,
    current_user: dict = Depends(get_current_user)
):

    account = await account_service.read_one(account_id)
    if not account or account.user_id != current_user["user_id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    return await tx_service.read_all(account_id=account_id, limit=limit, skip=skip)
