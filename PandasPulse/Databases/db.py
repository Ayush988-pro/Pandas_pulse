from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = (
    "mysql+pymysql://root:%40Ayush0529@localhost:3306/pandaspulse"
)
engine = create_engine(DATABASE_URL)
session = sessionmaker(bind=engine,autoflush=False,autocommit=False)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
print("Database Connected")