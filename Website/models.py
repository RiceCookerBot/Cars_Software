from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import Integer, String,Date,Time,Float,Boolean
from . import db

class Base(DeclarativeBase):
    pass

class Cars(db.Model,Base):
    __tablename__ = 'cars'

    registration: Mapped[str] = mapped_column(String, primary_key=True,unique=True)
    brand: Mapped[str] = mapped_column(String, nullable=False)
    model: Mapped[str] = mapped_column(String, nullable=False)
    color: Mapped[str] = mapped_column(String,nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    available: Mapped[bool] = mapped_column(Boolean, nullable=False,default=True)
    sold: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    owner: Mapped[str] = mapped_column(String, nullable=False, default='Cars Software')

    
class Service(db.Model,Base):
    __tablename__ = 'service'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    #Secoundary key
    registration: Mapped[str] = mapped_column(String)
    date: Mapped[str] = mapped_column(Date, nullable=False)
    description: Mapped[str] = mapped_column(String,nullable=False)
    mechanic: Mapped[str] = mapped_column(String, nullable=False)
    customer: Mapped[str] = mapped_column(String, nullable=False)


class Users(db.Model, Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String,nullable=False)
    password: Mapped[str] = mapped_column(String,nullable=False)
    name: Mapped[str] = mapped_column(String,nullable=False)
    #Forgein Key for client table
    phoneNumber: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String,nullable=False)


#Table for storing client informastion
class Customer(db.Model, Base):
    __tablename__ = 'clients'
    phoneNumber: Mapped[str] = mapped_column(String, nullable=False,primary_key=True)
    name: Mapped[str] = mapped_column(String,nullable=False)
    lastname: Mapped[str] = mapped_column(String)
    epost: Mapped[str] = mapped_column(String)
    address: Mapped[str] = mapped_column(String)
    postnumber: Mapped[str] = mapped_column(String)
