import requests

from pokemon.adapter.queries import query_pokemon_by_location
from pokemon.domain.repository import AbstractPokemonAdapter


class PokeAPIAdapter(AbstractPokemonAdapter):

    def __init__(self):
        self.url = 'https://beta.pokeapi.co/graphql/v1beta'

    def get_location_data(self, location: str) -> dict:
        variables = {
          "region": "kanto",
          "location": location
        }
        response = requests.post(url=self.url, json={"query": query_pokemon_by_location, "variables": variables})
        if response.status_code in range(200, 300):
            response_json = response.json()
            data = response_json.get("data", {})
            return data

