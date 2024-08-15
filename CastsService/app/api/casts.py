import logging
from fastapi import APIRouter, HTTPException, Depends, FastAPI
from typing import List

from CastsService.app.models.models import CastOut, CastIn
from CastsService.app.db import db_manager
from CastsService.app.db.db import init_db, close_db

from CastsService.app.models.models import CastOut, CastIn
from CastsService.app.db import db_manager

# Initialize the APIRouter for casts
casts = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@casts.post('/', response_model=CastOut, status_code=201)
async def create_cast(payload: CastIn):
    cast_id = await db_manager.add_cast(payload)
    
    response = CastOut(id=cast_id, **payload.dict())
    
    logger.info(f"Created cast entry with ID: {cast_id}")
    return response

@casts.get('/{id}/', response_model=CastOut)
async def get_cast(id: int):
    cast = await db_manager.get_cast(id)
    if not cast:
        logger.error(f"Cast entry with ID {id} not found")
        raise HTTPException(status_code=404, detail="Cast not found")
    
    logger.info(f"Retrieved cast entry with ID: {id}")
    return CastOut(**cast)
