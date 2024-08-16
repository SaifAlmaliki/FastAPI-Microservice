from fastapi import FastAPI
from app.api.casts import casts
from app.db.db import metadata, database, engine
from contextlib import asynccontextmanager

# Create all database tables
metadata.create_all(engine)

# Define the lifespan context manager for connecting/disconnecting the database
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect to the database when the application starts
    await database.connect()
    yield
    # Disconnect from the database when the application stops
    await database.disconnect()

# Initialize the FastAPI application with the lifespan context manager
app = FastAPI(lifespan=lifespan, openapi_url="/api/v1/casts/openapi.json", docs_url="/api/v1/casts/docs")

# Include the casts router with a specific prefix and tags
app.include_router(casts, prefix='/api/v1/casts', tags=['casts'])
