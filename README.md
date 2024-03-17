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