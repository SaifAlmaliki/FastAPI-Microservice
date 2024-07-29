import logging
from app.api.models import CastIn
from app.api.db import casts, database

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add a new cast entry to the database
async def add_cast(payload: CastIn) -> int:
    logger.info("Adding a new cast entry to the database")
    query = casts.insert().values(**payload.dict())
    cast_id = await database.execute(query=query)
    logger.info(f"Added new cast entry with ID: {cast_id}")
    return cast_id

# Retrieve a cast entry from the database by its ID
async def get_cast(id: int):
    logger.info(f"Retrieving cast entry with ID: {id}")
    query = casts.select().where(casts.c.id == id)
    cast = await database.fetch_one(query=query)
    
    if cast:
        logger.info(f"Retrieved cast entry with ID: {id}")
    else:
        logger.warning(f"Cast entry with ID {id} not found")
    
    return cast
