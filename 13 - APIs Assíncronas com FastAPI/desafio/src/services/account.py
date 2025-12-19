from typing import List

from databases.interfaces import Record
from sqlalchemy import insert, select

from src.database import database
from src.models.account import accounts
from src.schemas.account import AccountIn


class AccountService:
    async def read_all(self, limit: int = 100, skip: int = 0) -> List[Record]:

        query = select(accounts).limit(limit).offset(skip)
        return await database.fetch_all(query)

    async def create(self, account: AccountIn) -> Record:

        if account.balance < 0:
            raise ValueError("Initial balance cannot be negative")

        command = insert(accounts).values(
            user_id=account.user_id,
            balance=account.balance
        ).returning(accounts)

        created_account = await database.fetch_one(command)
        return created_account
