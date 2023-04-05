from fastapi import HTTPException

from pokemon.application.model import TourData, TourResponse, LocationDataScheme
from pokemon.domain.exceptions import WrongKantoLocation
from pokemon.domain.repository import AbstractPokemonAdapter


class PokemonTourService:

    def __init__(self, adapter: AbstractPokemonAdapter):
        self.adapter = adapter

    @staticmethod
    def _get_total_pokemon(area: dict) -> int:
        aggregate_data = area.get('aggregate_data', {})
        info = aggregate_data.get('info', {})
        return info.get('count', 0)

    def _get_info_by_location(self, location: str) -> LocationDataScheme:
        data = self.adapter.get_location_data(location=location)

        locations = data.get("locations", [])
        if not locations:
            raise WrongKantoLocation(f'{location} is not a Kanto location')

        location_json = locations[0]
        location_data = LocationDataScheme(**location_json)
        return location_data

    def get_data_from_tour(self, tour_data: TourData) -> TourResponse:
        locations = []
        try:
            for location in tour_data.planing_route:
                locations.append(self._get_info_by_location(location=location))
            response = TourResponse(
                locations=locations,
            )
            return response
        except WrongKantoLocation as e:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": str(e)
                }
            )


