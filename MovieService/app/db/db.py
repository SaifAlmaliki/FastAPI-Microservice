import os
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine, ARRAY
from databases import Database

# Fetch the DATABASE_URI environment variable
DATABASE_URI = os.getenv('DATABASE_URI')

if not DATABASE_URI:
    raise ValueError("No DATABASE_URI environment variable set")

# Function to create and return a SQLAlchemy engine
def get_engine():
    try:
        engine = create_engine(
            DATABASE_URI, 
            pool_size=10, 
            max_overflow=20, 
            pool_pre_ping=True,  # Ensures connections are valid before using them
            echo=False  # Set to True if you want to see generated SQL queries for debugging
        )
        return engine
    except Exception as e:
        raise RuntimeError(f"Error creating database engine: {e}")

# Create the SQLAlchemy engine
engine = get_engine()

# Initialize the metadata object to hold information about tables and schemas
metadata = MetaData()

# Define the 'movies' table schema using SQLAlchemy's Table, Column, and types
movies = Table(
    "movies", 
    metadata, 
    Column('id', Integer, primary_key=True),
    Column('name', String(50), nullable=False),
    Column('plot', String(250), nullable=False),
    Column('genres', ARRAY(String)),
    Column('casts_id', ARRAY(Integer))
)

# Create a Database instance from the databases package to interact with the database asynchronously
database = Database(DATABASE_URI)