from sqlalchemy import Column, String, JSON
from .database import Base

class Rail(Base):
    __tablename__ = 'rails'
    id = Column(String, primary_key=True, index=True)
    connections = Column(JSON)
    status = Column(String)
    coordinates = Column(JSON)
