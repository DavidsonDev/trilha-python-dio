from decimal import Decimal
from databases.interfaces import Record
from src.database import database
from src.exceptions import AccountNotFoundError, BusinessError
from src.models.account import accounts
from src.models.transaction import TransactionType, transactions
from src.schemas.transaction import TransactionIn


class TransactionService:
    async def read_all(self, account_id: int, limit: int = 100, skip: int = 0) -> list[Record]:
        query = transactions.select().where(transactions.c.account_id == account_id).limit(limit).offset(skip)
        return await database.fetch_all(query)

    @database.transaction()
    async def create(self, transaction: TransactionIn, user_id: int) -> Record:
 
        query = accounts.select().where(accounts.c.id == transaction.account_id)
        account = await database.fetch_one(query)
        if not account:
            raise AccountNotFoundError(f"Account {transaction.account_id} not found")

        if account.user_id != user_id:
            raise BusinessError(f"User {user_id} cannot modify account {transaction.account_id}")

        current_balance = Decimal(account.balance)
        amount = Decimal(transaction.amount)

        if transaction.type == TransactionType.WITHDRAWAL:
            new_balance = current_balance - amount
            if new_balance < 0:
                raise BusinessError("Insufficient balance for withdrawal")
        else:
            new_balance = current_balance + amount

        transaction_id = await self.__register_transaction(transaction)
        await self.__update_account_balance(transaction.account_id, new_balance)

        query = transactions.select().where(transactions.c.id == transaction_id)
        return await database.fetch_one(query)

    async def __update_account_balance(self, account_id: int, balance: Decimal) -> None:
        command = accounts.update().where(accounts.c.id == account_id).values(balance=balance)
        await database.execute(command)

    async def __register_transaction(self, transaction: TransactionIn) -> int:
        command = transactions.insert().values(
            account_id=transaction.account_id,
            type=transaction.type.value,
            amount=transaction.amount,
        )
        return await database.execute(command)
