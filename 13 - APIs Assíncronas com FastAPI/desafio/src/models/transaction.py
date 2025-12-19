from enum import Enum
import sqlalchemy as sa
from sqlalchemy import CheckConstraint
from src.database import metadata


class TransactionType(str, Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"


transactions = sa.Table(
    "transactions",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("account_id", sa.Integer, sa.ForeignKey("accounts.id"), nullable=False, index=True),
    sa.Column(
        "type",
        sa.Enum(TransactionType, name="transaction_types"),
        nullable=False
    ),
    sa.Column("amount", sa.Numeric(12, 2), nullable=False),
    sa.Column(
        "timestamp",
        sa.TIMESTAMP(timezone=True),
        nullable=False,
        server_default=sa.func.now()
    ),
    CheckConstraint("amount > 0", name="check_amount_positive"),
)
