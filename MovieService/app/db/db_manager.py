from typing import List, Optional
from app.models.models import MovieIn, MovieOut, MovieUpdate
from app.db.db import movies, database
import logging
from sqlalchemy.exc import SQLAlchemyError


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to add a new movie to the database
async def add_movie(payload: MovieIn) -> int:
    logger.info("Adding a new movie to the database")
    query = movies.insert().values(**payload.dict())
    try:
        result = await database.execute(query=query)
        logger.info("Added movie with id %d", result)
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error adding movie: {e}")
        raise

# Function to fetch all movies from the database
async def get_all_movies() -> List[MovieOut]:
    logger.info("Fetching all movies from the database")
    query = movies.select()
    try:
        result = await database.fetch_all(query=query)
        logger.info("Fetched %d movies", len(result))
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error fetching movies: {e}")
        raise

# Function to fetch a single movie by ID
async def get_movie(id: int) -> Optional[MovieOut]:
    logger.info("Fetching movie with id %d", id)
    query = movies.select().where(movies.c.id == id)
    try:
        result = await database.fetch_one(query=query)
        if result:
            logger.info("Movie with id %d found", id)
        else:
            logger.warning("Movie with id %d not found", id)
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error fetching movie with id {id}: {e}")
        raise

# Function to delete a movie by ID
async def delete_movie(id: int) -> int:
    logger.info("Deleting movie with id %d", id)
    query = movies.delete().where(movies.c.id == id)
    try:
        result = await database.execute(query=query)
        logger.info("Deleted movie with id %d", id)
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error deleting movie with id {id}: {e}")
        raise

# Function to update a movie by ID
async def update_movie(id: int, payload: MovieUpdate) -> int:
    logger.info("Updating movie with id %d", id)
    query = (
        movies
        .update()
        .where(movies.c.id == id)
        .values(**payload.dict(exclude_unset=True))
    )
    try:
        result = await database.execute(query=query)
        logger.info("Updated movie with id %d", id)
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error updating movie with id {id}: {e}")
        raise

# Optional: Add a function to handle bulk inserts
async def add_movies_bulk(payloads: List[MovieIn]) -> None:
    logger.info("Adding multiple movies to the database in bulk")
    query = movies.insert()
    values = [payload.dict() for payload in payloads]
    try:
        await database.execute_many(query=query, values=values)
        logger.info("Added %d movies in bulk", len(values))
    except SQLAlchemyError as e:
        logger.error(f"Error adding movies in bulk: {e}")
        raise
