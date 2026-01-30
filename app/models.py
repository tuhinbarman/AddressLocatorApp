from database import Base
from sqlalchemy import (
    String,Column,Integer,DateTime,Text,Float,ForeignKey)


class Address(Base):
    __tablename__ = "address"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,nullable=False)
    city = Column(String,nullable=False)
    state = Column(String,nullable=False)
    country = Column(String,nullable=False)
    latitude = Column(Float,nullable= False)
    longitude = Column(Float,nullable=False)