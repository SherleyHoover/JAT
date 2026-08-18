from .base import FlightProvider

from flights.models import Flight


class FictionalFlightProvider(
    FlightProvider
):

    def search(self, request):

        flights = Flight.objects.all()


        if request.get("origin"):

            flights = flights.filter(
                segments__departure_airport__iata_code=
                request["origin"]
            )


        if request.get("destination"):

            flights = flights.filter(
                segments__arrival_airport__iata_code=
                request["destination"]
            )


        return flights