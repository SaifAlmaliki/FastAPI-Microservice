from typing import List
from fastapi import HTTPException, APIRouter
import logging
from app.api.models import MovieIn, MovieOut, MovieUpdate
from app.api import db_manager
from app.api.service import is_cast_present

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create an APIRouter instance for the movies endpoints
movies = APIRouter()

# POST endpoint to add a new movie to the database
@movies.post('/', response_model=MovieOut, status_code=201)
async def create_movie(payload: MovieIn):
    for cast_id in payload.casts_id:
        if not is_cast_present(cast_id):
            raise HTTPException(status_code=404, detail=f"Cast with id:{cast_id} not found")

    movie_id = await db_manager.add_movie(payload)
    response = {
        'id': movie_id,
        **payload.dict()
    }
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
            if not is_cast_present(cast_id):
                logger.warning(f"Cast with id {cast_id} not found")
                raise HTTPException(status_code=404, detail=f"Cast with given id:{cast_id} not found")

    movie_in_db = MovieIn(**movie)
    updated_movie = movie_in_db.model_copy(update=update_data)

    updated_id = await db_manager.update_movie(id, updated_movie)
    logger.info(f"Updated movie with id {updated_id}")
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
