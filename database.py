from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Base

# PostgreSQL Bonus +10
# Örnek bağlantı
DATABASE_URL = "postgresql://postgres:1234@localhost:5432/movies"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
DATABASE_URL = "sqlite:///movie_archive.db"

