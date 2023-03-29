from src.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator


SQLALCHEMY_DATABASE_URI = Config.SQLALCHEMY_DATABASE_URI
 
try:      
    engine = create_engine(SQLALCHEMY_DATABASE_URI)

except Exception as ex:
        print("Connection could not be made due to the following error: \n", ex)

SessionLocal = sessionmaker(autocommit =False, autoflush=False,bind=engine)
Base = declarative_base()

# Dependency Injection
def get_db() -> Generator:
    try:
        db =SessionLocal()
        yield db
    finally:
         db.close()
    
