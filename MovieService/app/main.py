from fastapi import FastAPI, Depends
from app.api.movies import movies
from MovieService.app.db.db import metadata, database, engine
from contextlib import asynccontextmanager

# Create all database tables based on metadata definitions
metadata.create_all(engine)

# Define the lifespan context manager for managing the application's startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect to the database when the application starts
    await database.connect()
    yield
    # Disconnect from the database when the application stops
    await database.disconnect()

# Initialize the FastAPI application with the lifespan context manager
app = FastAPI(lifespan=lifespan, openapi_url="/api/v1/movies/openapi.json", docs_url="/api/v1/movies/docs")

# Include the movies router with a specific URL prefix and tags for better organization
app.include_router(movies, prefix='/api/v1/movies', tags=['movies'])
