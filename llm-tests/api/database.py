from sqlalchemy import create_engine, MetaData
from databases import Database
from config import TAGGING_POSTGRES_DB, TAGGING_POSTGRES_USER, TAGGING_POSTGRES_PASSWORD

DATABASE_URL = f"postgresql://{TAGGING_POSTGRES_USER}:{TAGGING_POSTGRES_PASSWORD}@tagging-db:5432/{TAGGING_POSTGRES_DB}"
# print(DATABASE_URL)
engine = create_engine(DATABASE_URL)
metadata = MetaData()
database = Database(DATABASE_URL)