import sqlalchemy as sa
from sqlalchemy import CheckConstraint
from src.database import metadata

accounts = sa.Table(
    "accounts",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("user_id", sa.Integer, nullable=False, index=True),
    sa.Column("balance", sa.Numeric(12, 2), nullable=False, default=0),
    sa.Column(
        "created_at",
        sa.TIMESTAMP(timezone=True),
        nullable=False,
        server_default=sa.func.now(), 
    ),
    CheckConstraint("balance >= 0", name="check_balance_positive"),
)
