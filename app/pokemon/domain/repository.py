from abc import ABC, abstractmethod


class AbstractPokemonAdapter(ABC):

    @abstractmethod
    def get_location_data(self, location: str) -> dict:
        ...
