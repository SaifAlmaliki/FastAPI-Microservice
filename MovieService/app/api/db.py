import os
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine, ARRAY
from databases import Database

# Fetch the DATABASE_URI environment variable
DATABASE_URI = os.getenv('DATABASE_URI')

if not DATABASE_URI:
    raise ValueError("No DATABASE_URI environment variable set")

# Create a SQLAlchemy engine to connect to the database
engine = create_engine(DATABASE_URI)

# Initialize the metadata object to hold information about tables and schemas
metadata = MetaData()

# Define the 'movies' table schema using SQLAlchemy's Table, Column, and types

movies = Table(
    "movies", 
    metadata, 
    Column('id', Integer, primary_key=True),
    Column('name', String(50)),
    Column('plot', String(250)),
    Column('genres', ARRAY(String)),
    Column('casts_id', ARRAY(Integer))
)

# Create a Database instance from the databases package to interact with the database asynchronously
database = Database(DATABASE_URI)