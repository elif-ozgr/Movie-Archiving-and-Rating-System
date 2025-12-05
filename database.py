from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models.models import Base
from sqlalchemy.exc import OperationalError

# MySQL bağlantısı (PyMySQL kullanılıyor)
DATABASE_URL = "mysql+pymysql://mdb:Md123456@localhost:3306/Movie_Rating_Archiving_System"

# Önce MySQL'e bağlanıp veritabanını kontrol/oluştur
engine_temp = create_engine("mysql+pymysql://mdb:Md123456@localhost:3306/")
with engine_temp.connect() as conn:
    try:
        # SQLAlchemy 2.x için text() kullanıyoruz
        conn.execute(text("CREATE DATABASE IF NOT EXISTS Movie_Rating_Archiving_System"))
    except OperationalError as e:
        print("Veritabanı oluşturulamadı:", e)

# Asıl engine
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Tüm tabloları oluşturur. Zaten varsa hata vermez."""
    try:
        Base.metadata.create_all(bind=engine)
        print("Tüm tablolar başarılı şekilde oluşturuldu veya zaten mevcut.")
    except Exception as e:
        print("Tablolar oluşturulamadı:", e)
