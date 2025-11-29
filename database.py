from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Base

# MySQL bağlantısı (PyMySQL kullanılıyor)
DATABASE_URL = "mysql+pymysql://mdb:Md123456@localhost:3306/Movie_Rating_Archiving_System"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)


