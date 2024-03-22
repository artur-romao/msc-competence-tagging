from sqlalchemy import Table, Column, Integer, String, create_engine
from sqlalchemy.dialects.postgresql import ARRAY
from database import metadata

Course = Table(
    "courses",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("course_name", String),
    Column("objectives", String),
    Column("contents", String),
    Column("skills", ARRAY(String)),
)
