from src.database import Base, engine
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship

# __tablename__ & 1 column is neccesary for creating table.
class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(300), nullable=False)
    is_active = Column(Boolean, default=True)
    items = relationship("Items", back_populates="owner")

class Items(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(80), unique=True, index=True, nullable=False)
    description = Column(String(300))
    date_posted = Column(Date)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("Users", back_populates="items")

#Base.metadata.create_all(bind = engine)
def applyMigrations():
    Base.metadata.create_all(bind = engine)