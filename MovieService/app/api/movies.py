from typing import List
from fastapi import HTTPException, APIRouter
import logging
from MovieService.app.models.models import MovieIn, MovieOut, MovieUpdate
from MovieService.app.db import db_manager
from MovieService.app.s2s.service import is_cast_present

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create an APIRouter instance for the movies endpoints
movies = APIRouter()

# POST endpoint to add a new movie to the database
@movies.post('/', response_model=MovieOut, status_code=201)
async def create_movie(payload: MovieIn):
    for cast_id in payload.casts_id:
        if not await is_cast_present(cast_id):  # Ensure async check
            logger.warning(f"Cast with id {cast_id} not found")
            raise HTTPException(status_code=404, detail=f"Cast with id:{cast_id} not found")

    movie_id = await db_manager.add_movie(payload)
    response = MovieOut(id=movie_id, **payload.dict())
    logger.info(f"Added movie with id {movie_id}")
    return response

# GET endpoint to return the list of all movies
@movies.get('/', response_model=List[MovieOut])
async def get_movies():
    movies_list = await db_manager.get_all_movies()
    logger.info(f"Fetched {len(movies_list)} movies")
    return movies_list

# GET endpoint to fetch a single movie by ID
@movies.get('/{id}/', response_model=MovieOut)
async def get_movie(id: int):
    movie = await db_manager.get_movie(id)
    if not movie:
        logger.warning(f"Movie with id {id} not found")
        raise HTTPException(status_code=404, detail="Movie not found")
    logger.info(f"Fetched movie with id {id}")
    return movie

# PUT endpoint to update an existing movie by ID
@movies.put('/{id}/', response_model=MovieOut)
async def update_movie(id: int, payload: MovieUpdate):
    movie = await db_manager.get_movie(id)
    if not movie:
        logger.warning(f"Movie with id {id} not found")
        raise HTTPException(status_code=404, detail="Movie not found")

    update_data = payload.dict(exclude_unset=True)

    if 'casts_id' in update_data:
        for cast_id in payload.casts_id:
            if not await is_cast_present(cast_id):
                logger.warning(f"Cast with id {cast_id} not found")
                raise HTTPException(status_code=404, detail=f"Cast with given id:{cast_id} not found")

    updated_movie = await db_manager.update_movie(id, payload)
    logger.info(f"Updated movie with id {id}")
    return updated_movie

# DELETE endpoint to remove a movie by ID
@movies.delete('/{id}', response_model=None)
async def delete_movie(id: int):
    movie = await db_manager.get_movie(id)
    if not movie:
        logger.warning(f"Movie with id {id} not found")
        raise HTTPException(status_code=404, detail="Movie not found")
    await db_manager.delete_movie(id)
    logger.info(f"Deleted movie with id {id}")
    return None
