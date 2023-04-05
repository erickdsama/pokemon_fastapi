from typing import List, Optional, Any

from pydantic import BaseModel, root_validator, Field


class Pokemon(BaseModel):
    name: str
    is_legendary: bool = False
    is_mythical: bool = False


class AreaData(BaseModel):
    name: str
    pokemon: List[Pokemon] = []
    total_species_pokemon: int = 0


class LocationData(BaseModel):
    areas: List[AreaData] = []
    name: str
