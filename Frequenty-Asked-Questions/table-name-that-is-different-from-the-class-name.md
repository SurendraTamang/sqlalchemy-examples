# How to name table different from defined Class Name?
In SQLAlchemy, when you're using the ORM (Object Relational Mapper) to map Python classes to database tables, you can easily specify a table name that is different from the class name. This is a common scenario when the table already exists in the database with a specific naming convention or when you want to adhere to certain naming standards in your database schema versus your Python code.

Here's how to declare a table name that differs from the class name:

```python
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine

Base = declarative_base()

class User(Base):
    # Specify the name of the table in the database as 'user_accounts'
    __tablename__ = 'user_accounts'
    
    # Define the columns
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
```

In this example, the class `User` is mapped to a table named `user_accounts` in the database. The `__tablename__` attribute within the class definition explicitly sets the name of the table.

### Using Attributes with Different Column Names

Sometimes, you might also want to have attribute names in your class that differ from the column names in your database table. SQLAlchemy allows you to specify a custom column name using the `name` argument in the `Column` definition.

```python
class User(Base):
    __tablename__ = 'user_accounts'
    
    # Define columns with custom column names in the database
    id = Column(Integer, primary_key=True)
    username = Column(String, name='user_name')  # The column in the database is 'user_name'
    emailaddress = Column(String, name='email_address')  # The column in the database is 'email_address'
```

In this modified example, the `User` class has attributes named `username` and `emailaddress`, but they are mapped to columns named `user_name` and `email_address` in the `user_accounts` table, respectively.

These features provide you with the flexibility to define your class model in a way that best fits your application's code style and naming conventions while still mapping correctly to existing database schemas or preferred database naming standards.