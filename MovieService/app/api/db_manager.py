from typing import List, Optional
from app.api.models import MovieIn, MovieOut, MovieUpdate
from app.api.db import movies, database
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to add a new movie to the database
async def add_movie(payload: MovieIn) -> int:
    logger.info("Adding a new movie to the database")
    query = movies.insert().values(**payload.dict())
    result = await database.execute(query=query)
    logger.info("Added movie with id %d", result)
    return result

# Function to fetch all movies from the database
async def get_all_movies() -> List[MovieOut]:
    logger.info("Fetching all movies from the database")
    query = movies.select()
    result = await database.fetch_all(query=query)
    logger.info("Fetched %d movies", len(result))
    return result

# Function to fetch a single movie by ID
async def get_movie(id: int) -> Optional[MovieOut]:
    logger.info("Fetching movie with id %d", id)
    query = movies.select().where(movies.c.id == id)
    result = await database.fetch_one(query=query)
    if result:
        logger.info("Movie with id %d found", id)
    else:
        logger.info("Movie with id %d not found", id)
    return result

# Function to delete a movie by ID
async def delete_movie(id: int) -> int:
    logger.info("Deleting movie with id %d", id)
    query = movies.delete().where(movies.c.id == id)
    result = await database.execute(query=query)
    logger.info("Deleted movie with id %d", id)
    return result

# Function to update a movie by ID
async def update_movie(id: int, payload: MovieUpdate) -> int:
    logger.info("Updating movie with id %d", id)
    query = (
        movies
        .update()
        .where(movies.c.id == id)
        .values(**payload.dict(exclude_unset=True))
    )
    result = await database.execute(query=query)
    logger.info("Updated movie with id %d", id)
    return result
