import json

from main import app
from pokemon.adapter.api_adapter import PokeAPIAdapter
from pokemon.domain.repository import AbstractPokemonAdapter
from test_main import client

headers = {'Content-type': 'application/json'}


class FakePokeApiAdapter(AbstractPokemonAdapter):

    def get_location_data(self, location: str) -> dict:
        with open('/test/pokemon/tests/fake_api_data.json', 'r') as fake_data:
            json_data = json.load(fake_data)
            data_response = json_data.get("data", {})

            data = next(filter((lambda loc: loc.get("name") == location), data_response.get('locations', [])), None)
        if data:
            return {
                "locations": [data]
            }
        return {
            "locations": []
        }


app.dependency_overrides[PokeAPIAdapter] = FakePokeApiAdapter


def test_routing_success():
    data = {
        "planing_route": [
            "viridian-forest",
            "birth-island",
            "pallet-town",
            "kanto-route-22",
            "rock-tunnel",
            "digletts-cave"
        ]
    }
    response = client.post("/v1/pokemon-in-location/", data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    assert response.json()['best_area']
    # gets the best area, based in the area with more diversity of Pokémon
    assert response.json()['interesting_area']
    # gets the most interesting area, based in the area with legendary or mythical Pokémon


def test_kanto_wrong_location():
    data = {
        "planing_route": [
            "roaming-johto",  # Region of johto :(
            "birth-island",
            "pallet-town",
            "kanto-route-22",
            "digletts-cave"
        ]
    }
    response = client.post("/v1/pokemon-in-location/", data=json.dumps(data), headers=headers)
    assert response.status_code == 400
