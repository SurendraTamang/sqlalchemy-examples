# SQLAlchemy
## Introduction



SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.

---

let's break it down into simpler terms.

Imagine you have a toy box (your database) where you keep all your toys (data). Now, you could just reach in and grab whatever toy you want by hand (using SQL directly), which is pretty straightforward but requires you to know exactly where each toy is.

SQLAlchemy is like having a magical robot friend who knows both your language and the layout of the toy box perfectly. You can tell this robot, "I want my toy car" or "Please put this new action figure in the right spot," using your everyday language (Python). The robot understands this and does the searching or organizing in the toy box for you, using its knowledge of the toy box's layout (SQL).

So, SQLAlchemy serves two main roles:

1. **Python SQL Toolkit**: As a toolkit, it's like giving your robot friend a set of tools to work more efficiently with the toys. This means you can still decide exactly how to organize or retrieve toys if you want to, using specific instructions. It's for when you need to be very precise about what you want to do with your data.

2. **Object Relational Mapper (ORM)**: The ORM part is about translating your requests into the robot's language automatically. It lets you work with your toys (data) using concepts you're familiar with, like objects in Python, without worrying about the details of how those toys are stored or retrieved from the box. This makes it easier to work with your data without knowing all the complexities of SQL.

In summary, SQLAlchemy gives you a powerful and flexible way to interact with your database. You can choose to be very specific about how you manage your data or let SQLAlchemy handle the details for you, making it easier and more efficient to work with your databases in Python.

### Understanding SQLAlchemy
SQLAlchemy consists of two distinct components:

* Core: A fully featured SQL abstraction toolkit that provides a smooth layer over relational databases, allowing you to execute SQL statements through Python code.
* ORM (Object-Relational Mapping): Builds upon the Core and provides a high-level ORM for mapping Python classes to database tables, allowing you to interact with your database using Pythonic object-oriented models instead of writing SQL queries.


## Installation
```bash
pip install SQLAlchemy
```
While practicing I am creating seperate python environment by using **venv**

```bash
python3 -m venv .venv
```



### Good Standard Practices

When working with SQLAlchemy, following good standard practices not only makes your code more readable and maintainable but also leverages the power of SQLAlchemy and Python to their fullest. Here are key practices:

#### Structure Your Project

- **Models**: Define your database models in a dedicated module or package. Each model class should inherit from `Base` (an object provided by SQLAlchemy) and represent a table in your database.

```python
# models.py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
```

- **Database Session Management**: Use context managers or dependency injection (in web frameworks) to manage database sessions. This ensures sessions are properly opened and closed, reducing the risk of memory leaks or connection issues.

```python
# db_session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

engine = create_engine('sqlite:///mydatabase.db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

#### Interact with the Database

- **CRUD Operations**: Encapsulate CRUD (Create, Read, Update, Delete) operations in functions or methods. This abstraction makes it easier to interact with your database through high-level interfaces.

```python
# crud.py
from models import User
from db_session import db_session

def create_user(name, email):
    with db_session() as session:
        user = User(name=name, email=email)
        session.add(user)
        session.commit()
        return user

def get_user(user_id):
    with db_session() as session:
        return session.query(User).filter(User.id == user_id).first()
```

- **Migration Management**: Use a migration tool like Alembic to manage schema changes. This allows you to version your database schema alongside your application code, making it easier to track changes and ensure consistency across environments.

#### Use the ORM Wisely

- **Leverage Relationships**: Define relationships between models to make navigating your data model more intuitive and efficient.

```python
# models.py continued
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="posts")

User.posts = relationship("Post", order_by=Post.id, back_populates="user")
```

- **Query Optimization**: Be mindful of the N+1 query problem and use eager loading (`joinedload`, `subqueryload`) where appropriate to optimize your database access patterns.

#### Code Quality and Maintenance

- **Type Annotations**: Use Python's type annotations to enhance code readability and facilitate static analysis.
- **Testing**: Write unit and integration tests for your models and database interactions to ensure reliability and facilitate refactoring.
- **Documentation**: Document your models, database interactions, and any important logic to make your codebase more approachable to new developers or collaborators.



Declarative mapping in SQLAlchemy is a way to define your database models and their relationships using Python classes. It's part of the declarative system provided by SQLAlchemy's ORM layer, which simplifies the process of tying database tables to Python classes. By using declarative mapping, you can define the structure of your database directly within your Python code in a clear and concise manner.

### Key Concepts of Declarative Mapping

- **Models as Python Classes**: Each table in your database is represented as a Python class. These classes are defined using a declarative base class that SQLAlchemy provides through the `declarative_base()` function.

- **Table Metadata**: The structure of the database table (e.g., columns and data types) is represented through attributes on the class. SQLAlchemy uses this information to interact with the database table directly.

- **Relationships**: Declarative mapping also allows you to define relationships between tables in a Pythonic way, using attributes that represent the connections between models. This can greatly simplify the handling of foreign keys and related records.

### Example of Declarative Mapping

Here's a basic example that illustrates how declarative mapping works in SQLAlchemy:

```python
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Create the declarative base class
Base = declarative_base()

# Define a User model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    # Define a relationship to the Address model
    addresses = relationship("Address", back_populates="user")

# Define an Address model
class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    # Establish a relationship with the User model
    user = relationship("User", back_populates="addresses")

# Connect to the database (for example, an in-memory SQLite database)
engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()
```

In this example:
- `Base` is the declarative base class from which all model classes inherit.
- `User` and `Address` are model classes that represent the `users` and `addresses` tables in the database, respectively.
- The `__tablename__` attribute specifies the name of the table in the database.
- Columns are defined as class attributes using `Column`, specifying their data types and constraints (e.g., `primary_key=True`).
- The `relationship` function is used to define relationships between the models. For example, `User.addresses` and `Address.user` establish a two-way link between users and their addresses.

Declarative mapping makes it straightforward to work with databases in an object-oriented manner, allowing developers to focus on their application logic rather than the intricacies of SQL and database schema management.

### Engine in SQLAlchemy
In SQLAlchemy, the `engine` is a core component that serves as the main interface to the database. It is responsible for managing the database connections and executing SQL statements. The engine is essentially the foundation on which SQLAlchemy builds to perform its operations, acting as a mediator between the Python application and the database server.

### Key Functions of the Engine

- **Connection Management**: The engine maintains a pool of connections to the database, which it reuses as needed. This pooling mechanism is efficient because it reduces the overhead of establishing and tearing down connections for each database operation.

- **SQL Execution**: It sends SQL statements crafted by either the SQLAlchemy Core expression language or the ORM to the database for execution and retrieves results.

- **Transaction Management**: The engine provides transaction control, allowing operations to be executed within the scope of a transaction. This means that multiple operations can either all succeed together or fail together, maintaining data integrity.

- **Dialect Abstraction**: SQLAlchemy supports multiple database systems (like PostgreSQL, MySQL, SQLite, Oracle, and more). The engine abstracts the differences between these database systems through dialects. A dialect is a component that understands how to communicate with a specific type of database, including the nuances of SQL syntax and database-specific features.

### Creating an Engine

You create an engine by providing a database connection URL and, optionally, some configuration parameters. The connection URL specifies the database dialect and the connection arguments (like username, password, host, database name).

Here's an example of how to create an engine for a SQLite database:

```python
from sqlalchemy import create_engine

# Create an engine connected to a SQLite database file named example.db
engine = create_engine('sqlite:///example.db')
```

For a PostgreSQL database, the engine creation might look like this:

```python
engine = create_engine('postgresql://user:password@localhost/mydatabase')
```

### Using the Engine

While you can use the engine directly to execute SQL statements, it's more common in SQLAlchemy to use it indirectly through sessions (for ORM operations) or through connection objects (for Core operations). Here's a simple example using the engine to execute a raw SQL query directly:

```python
with engine.connect() as connection:
    result = connection.execute("SELECT * FROM my_table")
    for row in result:
        print(row)
```

However, in most cases, you'll interact with the database through the ORM or the SQLAlchemy Core, using sessions or the Table API, which abstracts away the direct use of connection objects.

### Conclusion of Engine

The engine in SQLAlchemy acts as a gateway between your Python application and the database. By handling connection pooling, transaction management, and dialect-specific SQL nuances, it enables developers to interact with different types of databases in a unified and efficient manner.

### Session in SQLAlchemy
Database session management is a critical aspect of interacting with databases in web applications and scripts, particularly when using an ORM like SQLAlchemy. A session in this context represents a 'workspace' for your objects, where you can add or modify them before committing those changes to the database. Effective session management ensures that your application uses database connections efficiently and maintains data consistency.

### Understanding SQLAlchemy Sessions

In SQLAlchemy, a session facilitates the conversation between your Python application and the database. It's responsible for:
- Holding a cache of objects that have been read from the database and tracking changes to those objects.
- Transacting: grouping a series of operations into atomic commits or rollbacks.
- Providing an interface to query the database and return result sets as objects.

### Creating a Session Factory

First, you need a session factory configured through a `Sessionmaker` instance, which is usually done once per application. This factory will be used to create session objects. You typically bind it to an engine, which is responsible for maintaining database connections.

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///example.db')  # Or other connection string
Session = sessionmaker(bind=engine)
```

### Using Sessions in Your Application

When you need to interact with the database, you instantiate a session, work with it, and then close it. Here’s a simplified workflow:

1. **Open a Session**: At the beginning of a request or operation, create a new session using the factory.
   
2. **Work with the Session**: Add, modify, or delete objects, or issue queries through the session.
   
3. **Commit or Rollback**: If you're happy with the changes, commit them to apply all changes to the database. If something goes wrong, you can rollback the session to undo all uncommitted changes.
   
4. **Close the Session**: Once the work is done, close the session to free up the connection and resources.

### Example Workflow

Here's a basic example showing how to use a session:

```python
# Assuming Session is already created as above and User is a defined model
session = Session()

# Create a new user
new_user = User(name='John Doe', email='john.doe@example.com')
session.add(new_user)

# Commit the transaction
session.commit()

# Query for the user
user = session.query(User).filter_by(name='John Doe').first()
print(user)

# Close the session
session.close()
```

### Best Practices

- **Scope Your Sessions**: Use a session for a single logical operation or request. Avoid sharing sessions between different threads or requests.
- **Manage Transactions**: Be explicit about when you commit or rollback transactions. It's usually best to commit late, ensuring that all operations have succeeded before applying changes to the database.
- **Automate Session Closure**: Use context managers or framework-specific hooks to ensure sessions are closed properly, even if errors occur.
- **Avoid Long-Lived Sessions**: Long-lived sessions can hold onto resources and prevent updates from being visible to other transactions. Aim to keep your sessions short-lived.

### Advanced Patterns

For more complex applications, especially web applications, you might use patterns like:
- **Session per request**: In web applications, a common pattern is to create a new session for each request and close it when the request is finished.
- **Dependency Injection**: Frameworks like FastAPI allow you to inject session instances into your route functions, ensuring that session lifecycle is managed according to the request lifecycle.

By following these practices and understanding how sessions work, you can effectively manage your database interactions in SQLAlchemy, ensuring efficient resource use and maintaining data integrity.


### MetaData
In SQLAlchemy, `MetaData` is a container object that holds together many different features of a database (or multiple databases) being described. When you're using SQLAlchemy, especially with the Core expression language, `MetaData` plays a crucial role in defining, accessing, and managing database schemas.

### Key Functions of `MetaData`:

- **Schema Definition**: `MetaData` is used to define the structure of the database, including tables, columns, data types, constraints (like primary keys, foreign keys), and indexes. Each `Table` object is associated with a `MetaData` instance.

- **Schema Reflection**: It can also be used to load the database schema from an existing database into SQLAlchemy objects. This process is known as reflection, and it allows SQLAlchemy to automatically generate `Table` and other schema objects based on the actual database structure.

- **Schema Creation and Dropping**: `MetaData` provides methods to create or drop the schema it contains on the database. This is useful for initializing databases from SQLAlchemy models and for testing or deployment purposes where you need to programmatically manage the database schema.

### Using `MetaData`:

Here's a simple example to illustrate how `MetaData` is used to define and create a database schema:

```python
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

# Create an engine (connection to a database)
engine = create_engine('sqlite:///example.db')

# Create a MetaData instance
metadata = MetaData()

# Define a table with the MetaData instance
users_table = Table('users', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('name', String),
                    Column('age', Integer))

# Create the table in the database
metadata.create_all(engine)
```

In this example:
- A `MetaData` instance is created to group the schema definitions.
- A `Table` object is defined, associated with the `MetaData` instance, which represents a table in the database with specific columns (`id`, `name`, and `age`).
- The `create_all` method of `MetaData` is called with an engine, which executes the necessary SQL commands to create the table in the database if it doesn't already exist.

### Reflection:

`MetaData` can also be used to reflect an existing database schema:

```python
# Reflect all tables from the database
metadata.reflect(engine)

# Access a table from the reflected metadata
users_table = metadata.tables['users']
```

This feature is particularly useful when working with existing databases, as it saves time and ensures that the SQLAlchemy objects match the current state of the database.

### Conclusion:

`MetaData` in SQLAlchemy is a central concept that enables the definition, reflection, and manipulation of database schemas. It provides a structured way to interact with the database structure through SQLAlchemy, making it an essential tool for Python developers working with relational databases.

### MetaData in ORM 
When defining ORM (Object-Relational Mapping) models in SQLAlchemy, `MetaData` plays a critical role, albeit in a more implicit manner compared to its use in the SQLAlchemy Core. In the ORM, `MetaData` is used behind the scenes to collect and organize information about the model classes (which represent database tables) and their fields (which represent columns in those tables). This allows SQLAlchemy to generate the appropriate SQL statements for creating schemas, querying data, and more.

### How `MetaData` is Used with ORM

When you use the declarative system in SQLAlchemy to define your ORM models, each model class inherits from a base class (commonly referred to as `Base` in SQLAlchemy documentation and examples) that is produced by the `declarative_base()` function. This `Base` class contains a `MetaData` object, and all the model classes that inherit from `Base` are automatically associated with this `MetaData` object.

Here's a simplified example to illustrate this:

```python
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine

# Create the base class using declarative_base()
Base = declarative_base()

# Define a model class
class User(Base):
    __tablename__ = 'users'  # Name of the table in the database
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

# Engine (connection to the database)
engine = create_engine('sqlite:///example.db')

# Create the database tables based on the models
Base.metadata.create_all(engine)
```

In this ORM example:
- The `declarative_base()` function generates a base class (`Base`) with its own `MetaData` instance.
- The `User` class inherits from `Base`, meaning it's automatically associated with `Base`'s `MetaData`. The `__tablename__` attribute specifies the table's name, and the `Column` objects define its columns.
- `Base.metadata.create_all(engine)` uses the `MetaData` to create the `users` table in the database, if it does not already exist. This step translates the model definitions into SQL statements that define the table schema.

### Why It Matters

Using `MetaData` implicitly through the ORM provides several benefits:
- **Simplification**: It abstracts away the manual handling of `MetaData`, making model definitions cleaner and more straightforward.
- **Centralization**: All model definitions are automatically registered with the `MetaData` object, centralizing schema information and making operations like creating or dropping tables efficient.
- **Flexibility**: You can still access the `MetaData` object directly through `Base.metadata` if you need to perform custom schema operations, reflect an existing database, or integrate with SQLAlchemy Core functionality.

In summary, while defining ORM models in SQLAlchemy, `MetaData` is managed implicitly, providing a seamless and efficient way to translate high-level Python class definitions into database schema operations.


#### Engine, Session workflow
Yes, that's right! When you're using SQLAlchemy, you usually start with two main concepts: the **engine** and the **session**. Let's go through them one by one in simple terms.

### 1. Engine

The engine is like the start button of your car or the power switch of your robot friend. It's the way you tell SQLAlchemy how to connect to your database. When you create an engine, you're essentially setting up the details about which database you're going to talk to, such as where it is (like a web address or a file on your computer) and how to log in.

Here's how you might set it up in Python code:

```python
from sqlalchemy import create_engine

# Create an engine that knows how to connect to your database
engine = create_engine('sqlite:///mydatabase.db')  # For a SQLite database stored in a file named "mydatabase.db"
```

This line of code doesn't actually connect to the database right away. It just sets up the details so SQLAlchemy knows how to connect when it needs to.

### 2. Session

Once your engine is ready, the next step is to start a session. You can think of a session as a conversation between your application (you) and the database (the toy box). During this conversation, you'll tell the database what you want to do, like adding new toys, changing them, or taking some out.

A session keeps track of all these requests and, when you're ready, it sends them all to the database at once. This is handy because it means the database doesn't have to update everything immediately each time you ask for a small change, making the whole process more efficient.

Here's a simple way to start a session:

```python
from sqlalchemy.orm import sessionmaker

# Create a sessionmaker bound to your engine
Session = sessionmaker(bind=engine)

# Start a new session
session = Session()
```

With the session started, you can now interact with your database. You can add new records, query for data, or update existing records. Here's a quick example of adding a new "toy":

```python
# Assuming you have a Toy class defined as a model
new_toy = Toy(name="Teddy Bear", color="Brown")
session.add(new_toy)

# Save the new toy to the database
session.commit()
```

And that's the gist of starting with SQLAlchemy! You set up an engine to know where and how to connect to your database, and then you start a session to talk to the database, telling it what you want to do.


#### Details about Session's commit
In simple terms, the `commit` method is like saying "Okay, let's make everything we just did official." When you're using a session in SQLAlchemy (or most database systems), you can think of all the changes you make (like adding a new toy to the box, painting an existing toy, or even deciding to give one away) as being in a temporary state. They're planned but not finalized. This is useful because it allows you to change your mind or correct mistakes before making anything permanent.

Here's a little breakdown:

### Before Committing
- **Adding or Modifying Data**: Imagine you're arranging toys in your room. You decide where everything should go, move a few things around, and maybe set aside some toys to donate. But until you actually put them in their new spots (or in the donation box), all these decisions are just plans.
- **Temporary State**: In database terms, all the changes you make during a session are kept in a "temporary" state. They're remembered by the session, but they haven't been applied to the database yet. This means nobody else who might be looking at your toys (or data) can see these changes; they still see everything as it was before you started.

### Committing
- **Making Changes Official**: When you're happy with all the changes you've made during your session, you call `commit`. This is like finally putting the toys in their new spots and taking the donation box out to the charity. You're making all your changes official and permanent.
- **Updating the Database**: Calling `commit` tells the session to send all the changes to the database. The database updates all the records accordingly, and now everyone who accesses it will see the updated state of things.

### After Committing
- **Changes Are Permanent**: Once you've committed your changes, they're part of the database. If you made a mistake, you would need to start a new session to make corrections (like deciding you actually didn't want to donate that one toy and buying it back).
- **Starting Fresh**: After committing, your session is like a clean slate. You can start making new changes, adding more toys, or whatever else you need to do. If you're done, you can close the session, knowing that all your changes are safe and sound in the database.

Here's how it looks in code when you're using SQLAlchemy:

```python
session.add(new_toy)  # Plan to add a new toy
session.commit()  # Make it official
```

So, `commit` is your way of telling the database, "Yes, I'm sure about these changes. Please update everything accordingly."


### Shall we close the session or close it?
Whether to close a session after committing changes or continue using it for additional operations depends on the context of your application and your specific needs. Here are a few considerations to help you decide:

### Closing a Session
- **Isolation**: If your operations require strict isolation from each other, closing the session after a commit ensures that subsequent operations start with a fresh state. This can be particularly important in scenarios where the consistency of data is critical after each set of operations.
- **Resource Management**: Closing a session when it's no longer needed can help with resource management, freeing up database connections and other resources. This is especially important in applications with high loads or limited resources.

### Continuing with the Same Session
- **Performance**: In some cases, it might be more efficient to keep using the same session for multiple operations, especially if those operations are closely related or dependent on each other. Opening and closing sessions repeatedly can introduce overhead.
- **Transactional Work**: If you're performing a series of operations that logically belong together as a unit of work, you might choose to keep the session open until all those operations are complete. You would commit the transaction to save the changes and then close the session.

### Best Practices

- **Explicit Control**: It's generally a good practice to have explicit control over when your sessions begin and end. This helps avoid unintended side effects and makes the flow of your application clearer.
- **Error Handling**: Always ensure proper error handling around your database operations. This includes potentially rolling back a session if an operation fails before you commit.
- **Session Lifecycle Management**: For web applications, you might use request-based session management, where a new session is created at the beginning of a web request and closed at the end of the request, ensuring that each request is handled in isolation.

### Example Patterns

**Short-Lived Sessions (Close After Commit)**
```python
# Perform an operation and then close the session
session.add(new_record)
session.commit()
session.close()  # Close the session to free resources
```

**Continued Use (Keep Session Open)**
```python
# Continue using the session for related operations
session.add(first_record)
session.commit()  # Commit the first set of changes

session.add(second_record)  # Continue using the same session
# Later...
session.commit()  # Commit subsequent changes
session.close()  # Close the session when done
```

In summary, whether to close a session immediately after committing changes or to continue using it depends on your application's requirements and the specific scenario at hand. Managing sessions correctly is key to ensuring your application interacts with the database efficiently and safely.

#### How to interact with Existing table in SQLAlchemy?
To use an existing table in a database with SQLAlchemy, you have a couple of options depending on whether you're using SQLAlchemy's Core or ORM component. Here's how you can declare or use an existing table with both:

### Using SQLAlchemy Core for Existing Tables

If you're working directly with SQLAlchemy Core, you can use the `Table` object to reflect (automatically load) the table's metadata from the database. This method doesn't require you to declare the column details manually.

```python
from sqlalchemy import create_engine, MetaData, Table

# Create an engine
engine = create_engine('sqlite:///mydatabase.db')

# Reflect the existing table
metadata = MetaData()
my_existing_table = Table('my_existing_table', metadata, autoload_with=engine)

# Now you can use `my_existing_table` to construct queries
```

### Using SQLAlchemy ORM for Existing Tables

If you're using SQLAlchemy's ORM, you'll typically map a class to an existing table using the `declarative_base` method combined with the `autoload_with` argument. However, with recent versions of SQLAlchemy, the preferred method is to use the `automap_base` function to automatically generate mapped classes from an existing database schema.

#### Reflecting Tables with Automap

```python
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

# Create an engine
engine = create_engine('sqlite:///mydatabase.db')

# Reflect the tables
Base = automap_base()
Base.prepare(engine, reflect=True)

# Access the mapped class
MyExistingTable = Base.classes.my_existing_table

# Now you can use `MyExistingTable` with a session to query the table
session = Session(engine)
for instance in session.query(MyExistingTable).limit(10):
    print(instance)
```

#### Manually Mapping a Class to an Existing Table

If you need more control or the automap doesn't suit your needs (e.g., if you want to add additional methods to the class), you can manually map a class to an existing table using the `Table` object with `autoload_with` and then declare your class using the `mapper` function.

```python
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, Session

engine = create_engine('sqlite:///mydatabase.db')
metadata = MetaData()

# Reflect the existing table
my_table = Table('my_existing_table', metadata, autoload_with=engine)

# Define the class to map to the table
class MyExistingTable:
    pass

# Map the class to the table
mapper(MyExistingTable, my_table)

# Now you can use `MyExistingTable` with a session to query the table
session = Session(engine)
for instance in session.query(MyExistingTable).limit(10):
    print(instance)
```

These examples show how to declare or use an existing table in SQLAlchemy, either with the Core or ORM approach. Choose the method that best fits your application's architecture and your preferred way of working with the database.