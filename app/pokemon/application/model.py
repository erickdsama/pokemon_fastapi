from typing import List, Optional, Any

from pydantic import BaseModel, root_validator

from pokemon.domain.model import AreaData, Pokemon, LocationData


class TourData(BaseModel):
    planing_route: list[str]

    class Config:

        schema_extra = {
            "planing_route": [
                "viridian-forest",
                "pallet-town",
                "kanto-route-22",
                "digletts-cave",
                "birth-island"
            ]
        }


class PokemonScheme(Pokemon):
    name: str
    is_legendary: bool = False
    is_mythical: bool = False

    def __init__(self, **data: Any):
        data = data.get('pokemon_v2_pokemon')
        if 'pokemon_v2_pokemonspecy' in data:
            specy = data['pokemon_v2_pokemonspecy']
            data['is_legendary'] = specy.get("is_legendary", False)
            data['is_mythical'] = specy.get("is_mythical", False)
        super().__init__(**data)


class AreaDataScheme(AreaData):
    pokemon: List[PokemonScheme] = []
    @property
    def interesting_pokemon(self) -> bool:
        """
        returns True or False if it finds a legendary or mythical Pokémon
        :return: bool
        """
        value = next(filter((lambda pokemon: pokemon.is_legendary or pokemon.is_mythical), self.pokemon), None)
        return value is not None

    @root_validator()
    def set_length_species(cls, values):
        pokemon = values.get('pokemon', [])
        if pokemon:
            values['total_species_pokemon'] = len(pokemon)
        return values

    def __gt__(self, other) -> bool:
        return self.total_species_pokemon > other.total_species_pokemon


class LocationDataScheme(LocationData):
    areas: List[AreaDataScheme]

    @property
    def greater_diversity_area(self) -> AreaData:
        """
        returns the most diversity AreaData find it
        :return: AreaData
        """
        value = max(self.areas, key=lambda area: area.total_species_pokemon)
        return value

    @property
    def interesting_area(self) -> AreaData:
        """
        returns an AreaData if it finds a legendary or mythical Pokémon
        :return: AreaData
        """
        value = next(filter((lambda area: area.interesting_pokemon), self.areas), None)
        return value

    def __gt__(self, other) -> bool:
        """
        compare the greater diversity area from one location and another location
        :param other: LocationData
        :return: True or False
        """
        return self.greater_diversity_area > other.greater_diversity_area


class TourResponse(BaseModel):
    best_area: Optional[AreaDataScheme] = None
    interesting_area: Optional[AreaDataScheme] = None
    locations: List[LocationDataScheme] = []

    class Config:
        validate_all = True

    @root_validator
    def validate_all_filled(cls, values) -> dict:
        """Set the best_area field based in locations data"""
        if values.get('locations'):
            best_location = max(values.get('locations', []))
            if best_location:
                values['best_area'] = best_location.greater_diversity_area

            interesting_location = next(
                filter((lambda location: location.interesting_area), values.get('locations', [])), None)
            if interesting_location:
                values["interesting_area"] = interesting_location.interesting_area
            return values

