from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Country

# Creating the engine 
# It will create the database of restaurants
engine = create_engine('sqlite:///countries.db')

with Session(engine) as session:
    country = Country(name="Nepal", continent="Asia", population=31143833)
    session.add(country)
    session.commit()
    print("Added successfully")