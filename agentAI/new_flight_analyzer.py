from flights.models import Airport_Data, Airline_Data
from .llm.deepseek import DeepSeekLLM
from .analyze.filter_regions import filter_by_airline_region
from .analyze.new_assess_points import summarize_flights

class newFlightAnalyzer:

    def __init__(self):
        self.llm = DeepSeekLLM()


    def new_analyze(
        self,
        flights,
        weights
    ):

        # 1. Filter by airline region

        flights = filter_by_airline_region(
            flights
        )


        # 2. Calculate scores

        flights = summarize_flights(
            flights,
            weights
        )


        # 3. Find airports

        airport_codes = set()

        for flight in flights:

            segments = flight[
                "segments"
            ]

            origin = (
                segments[0]
                ["departure_airport"]
                ["iata_code"]
            )

            destination = (
                segments[-1]
                ["arrival_airport"]
                ["iata_code"]
            )

            airport_codes.add(
                origin
            )

            airport_codes.add(
                destination
            )


        # 4. Find airlines

        airline_codes = set()

        for flight in flights:

            airline_codes.add(
                flight[
                    "airline"
                ]["iata_code"]
            )


        # 5. Database lookup

        airports = Airport_Data.objects.filter(
            iata_code__in=airport_codes
        )

        airlines = Airline_Data.objects.filter(
            iata_code__in=airline_codes
        )


        # 6. Convert to dictionaries

        airport_data = []

        for airport in airports:

            airport_data.append({
                "iata_code":
                    airport.iata_code,

                "name":
                    airport.name,

                "country":
                    airport.country
            })


        airline_data = []

        for airline in airlines:

            airline_data.append({
                "iata_code":
                    airline.iata_code,

                "name":
                    airline.name
            })


        print("FlightAnalyzer")
        #print(flights)
        return {
            "flights_filtered":
                flights,

            "weights":
                weights
        }