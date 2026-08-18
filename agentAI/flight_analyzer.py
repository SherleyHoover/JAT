# agent_ai/flight_analyzer.py

from flights.models import Airport_Data, Airline_Data
from .llm.deepseek import DeepSeekLLM
from .analyze.filter_regions import filter_by_airline_region
from .analyze.assess_points import summarize_flights

class FlightAnalyzer:

    def __init__(self):
        self.llm = DeepSeekLLM()


    def analyze(self, flights):
        #print(flights)
        # 1. Find all airports used by these flights
        airport_codes = set()
        flights = filter_by_airline_region(flights)
        print(flights)
        flights = summarize_flights(flights)
        for flight in flights:

         segments = flight["segments"]

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

        airport_codes.add(origin)
        airport_codes.add(destination)


        # 2. Find all airlines used by these flights
        airline_codes = set()

        for flight in flights:
            airline_codes.add(
                flight["airline"]["iata_code"]
            )


        # 3. Query database
        airports = Airport_Data.objects.filter(
            iata_code__in=airport_codes
        )

        airlines = Airline_Data.objects.filter(
            iata_code__in= airline_codes
        )


        # 4. Convert Django objects into dictionaries
        airport_data = []

        for airport in airports:
            airport_data.append(
                {
                    "iata_code": airport.iata_code,
                    "name": airport.name,
                    "country": airport.country,
                    
                }
            )


        airline_data = []

        for airline in airlines:
            airline_data.append(
                {
                    "iata_code": airline.iata_code,
                    "name": airline.name,
                    #"region": airline.region,
                }
            )

        print("FlightAnalyzer")
        # 5. Send everything to LLM
        return {"flights_filtered": flights
                }
       # return self.llm.generate(
        #    flight_data=flights,
         #   airport_data=airport_data,
          #  airline_data=airline_data
        #)