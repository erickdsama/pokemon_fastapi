from fastapi import APIRouter, Depends

from pokemon.adapter.api_adapter import PokeAPIAdapter
from pokemon.application.model import TourData, TourResponse
from pokemon.application.service import PokemonTourService
from pokemon.domain.repository import AbstractPokemonAdapter

tour_router = APIRouter(
    tags=['locations'],
    prefix='/pokemon-in-location'
)


@tour_router.post(path='/', status_code=200)
def get_pokemon_data(*, tour_data: TourData, pokemon_adapter: AbstractPokemonAdapter = Depends(PokeAPIAdapter)):
    serv = PokemonTourService(adapter=pokemon_adapter)
    return serv.get_data_from_tour(tour_data=tour_data)
