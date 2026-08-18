from abc import ABC, abstractmethod


class FlightProvider(ABC):

    @abstractmethod
    def search(self, request):
        raise NotImplementedError