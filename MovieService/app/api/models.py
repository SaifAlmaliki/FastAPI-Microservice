from typing import List, Optional
from pydantic import BaseModel

# Input model for a movie, used when adding a new movie
# This class represents the structure of a movie when inputting new movie data.
class MovieIn(BaseModel):
    name: str
    plot: str
    genres: List[str]
    casts_id: List[int]

# Output model for a movie, Inherits from MovieIn and extends it with an id field.
# Used when outputting movie data, including a unique identifier for the movie.
class MovieOut(MovieIn):
    id: int

# Update model for a movie, allows partial updates by making all fields optional
class MovieUpdate(MovieIn):
    name: Optional[str] = None
    plot: Optional[str] = None
    genres: Optional[List[str]] = None
    casts_id: Optional[List[int]] = None
