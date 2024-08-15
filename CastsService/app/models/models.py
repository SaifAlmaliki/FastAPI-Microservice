from typing import List, Optional
from pydantic import BaseModel

# Input model for creating a new cast
class CastIn(BaseModel):
    name: str 
    nationality: Optional[str] = None

# Output model for returning cast details, inherits from CastIn
class CastOut(CastIn):
    id: int

# Update model for updating an existing cast entry, inherits from CastIn
class CastUpdate(CastIn):
    name: Optional[str] = None
