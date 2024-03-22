from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy import create_engine,Column, Integer, String

# Creating the engine 
# It will create the database of restaurants, Enable echo will show the SQL queries
engine = create_engine('sqlite:///countries.db', echo=True)

class Base(DeclarativeBase):
    pass

class Country(Base):
    __tablename__ = "countries"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, name="Name", unique=True)
    continent = Column(String, name="Continent")
    population = Column(Integer, name="Population")



if __name__ == '__main__':

    # Create all which is on Base
    #Base.metadata.drop_all(engine)

    # Creating all 
        Base.metadata.create_all(engine)