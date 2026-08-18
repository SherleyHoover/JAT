from flights.services import FlightSearchService
from flights.serializers import FlightSerializer

def search_flights(
        origin,
        destination,
        max_price=None
):

    request = {
        "origin": origin,
        "destination": destination,
        "max_price": max_price,
    }

    service = FlightSearchService()

    results = service.search(request)
    serializer = FlightSerializer(
        results,
        many=True
    )
    return serializer.data