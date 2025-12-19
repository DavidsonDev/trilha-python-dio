import databases
import sqlalchemy as sa
from sqlalchemy.engine import URL

from src.config import settings

# URL
DATABASE_URL = settings.database_url

# Async database
database = databases.Database(DATABASE_URL)

metadata = sa.MetaData()

if "sqlite" in DATABASE_URL:
    
    engine = sa.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = sa.create_engine(DATABASE_URL)
