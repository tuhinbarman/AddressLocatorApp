from pydantic import BaseModel,Field
from typing import Optional

class AddressRequest(BaseModel):
    id : int 
    name: str = Field(max_length = 255)
    city: str = Field(max_length = 255)
    state: str = Field(max_length = 255)
    country: str = Field(max_length = 255)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(...,ge=-180, le=180)