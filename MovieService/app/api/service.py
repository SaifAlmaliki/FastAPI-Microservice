import os
import httpx
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the cast service URL from environment variables, or use the default if not set
url = os.environ.get('CAST_SERVICE_HOST_URL', 'http://localhost:8002/api/v1/casts/')

# Check if a cast member is present in the cast service
def is_cast_present(cast_id: int) -> bool:
    logger.info(f"Checking presence of cast member with id {cast_id} ...")
    request_url = f'{url}{cast_id}'
    logger.debug(f"Request URL: {request_url}")
    
    r = httpx.get(request_url)
    
    logger.debug(f"Response Status Code: {r.status_code}")
    logger.debug(f"Response Content: {r.text}")
    
    if r.status_code == 200:
        logger.info(f"Cast member with id {cast_id} is present")
        return True
    else:
        logger.warning(f"Cast member with id {cast_id} not found")
        return False
