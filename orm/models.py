from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy import create_engine,Column, Integer, String

# Creating the engine 
# It will create the database of restaurants
engine = create_engine('sqlite:///countries.db')

class Base(DeclarativeBase):
    pass

class Country(Base):
    __tablename__ = "countries"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, name="Name")
    continent = Column(String, name="Continent")
    population = Column(Integer, name="Population")


# Create all which is on Base
Base.metadata.create_all(engine)