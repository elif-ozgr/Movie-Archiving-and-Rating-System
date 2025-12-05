from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models.models import Base
from sqlalchemy.exc import OperationalError

# MySQL connection (using PyMySQL)
DATABASE_URL = "mysql+pymysql://mdb:Md123456@localhost:3306/Movie_Rating_Archiving_System"

# First, connect to MySQL and check/create the database
engine_temp = create_engine("mysql+pymysql://mdb:Md123456@localhost:3306/")
with engine_temp.connect() as conn:
    try:
        # Using text() for SQLAlchemy 2.x
        conn.execute(text("CREATE DATABASE IF NOT EXISTS Movie_Rating_Archiving_System"))
    except OperationalError as e:
        print("Database could not be created:", e)

# Main engine
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Creates all tables. Will not raise an error if they already exist."""
    try:
        Base.metadata.create_all(bind=engine)
        print("All tables successfully created or already exist.")
    except Exception as e:
        print("Tables could not be created:", e)
