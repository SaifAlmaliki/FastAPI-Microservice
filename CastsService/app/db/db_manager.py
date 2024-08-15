import logging
from sqlalchemy.exc import SQLAlchemyError
from CastsService.app.models.models import CastIn
from CastsService.app.db.db import casts, database

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Add a new cast entry to the database
async def add_cast(payload: CastIn) -> int:
    query = casts.insert().values(**payload.dict())
    try:
        cast_id = await database.execute(query=query)
        logger.info(f"Added new cast entry with ID: {cast_id}")
        return cast_id
    except SQLAlchemyError as e:
        logger.error(f"Error adding cast entry: {e}")
        raise

# Retrieve a cast entry from the database by its ID
async def get_cast(id: int):
    query = casts.select().where(casts.c.id == id)
    try:
        cast = await database.fetch_one(query=query)
        
        if cast:
            logger.info(f"Retrieved cast entry with ID: {id}")
        else:
            logger.warning(f"Cast entry with ID {id} not found")
        
        return cast
    except SQLAlchemyError as e:
        logger.error(f"Error retrieving cast entry with ID {id}: {e}")
        raise

# Optional: Add a function to handle bulk inserts
async def add_casts_bulk(payloads: list[CastIn]) -> None:
    query = casts.insert()
    values = [payload.dict() for payload in payloads]
    try:
        await database.execute_many(query=query, values=values)
        logger.info(f"Added {len(values)} cast entries in bulk.")
    except SQLAlchemyError as e:
        logger.error(f"Error adding cast entries in bulk: {e}")
        raise
