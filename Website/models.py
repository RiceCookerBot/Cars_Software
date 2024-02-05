from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import Integer, String,Date,Time
from . import db

class Base(DeclarativeBase):
    pass

class Cars(db.Model,Base):
    __tablename__ = 'cars'

    registration: Mapped[str] = mapped_column(String, primary_key=True,unique=True)
    #Forgein Key
    eier1: Mapped[str] = mapped_column(String,nullable=False)
    eier2: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String, nullable=False)
    model: Mapped[str] = mapped_column(String, nullable=False)

    
class Service(db.Model,Base):
    __tablename__ = 'service'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    #Secoundary key
    registration: Mapped[str] = mapped_column(String)
    date: Mapped[str] = mapped_column(Date, nullable=False)
    description: Mapped[str] = mapped_column(String,nullable=False)


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
class Clients(db.Model, Base):
    __tablename__ = 'clients'
    phoneNumber: Mapped[str] = mapped_column(String, nullable=False,primary_key=True)
    name: Mapped[str] = mapped_column(String,nullable=False)
    lastname: Mapped[str] = mapped_column(String)
    epost: Mapped[str] = mapped_column(String)
    homeAddress: Mapped[str] = mapped_column(String)
    postnumber: Mapped[str] = mapped_column(String)
