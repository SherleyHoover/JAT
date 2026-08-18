from flights.models import Airline_Data


def filter_by_airline_region(flights):
    #print(flights)
    # Find all airline codes used by the flights
    airline_codes = set()

    for flight in flights:
        airline_codes.add(
            flight["airline"]["iata_code"]
        )
    
    # Get the corresponding airlines from the database
    airlines = Airline_Data.objects.filter(
        iata_code__in=airline_codes
    )

    # Create a lookup:
    # IATA code -> True/False
    airline_status = {}

    for airline in airlines:
        airline_status[airline.iata_code] = airline.region_acceptable

    # Check whether at least one acceptable airline exists
    has_acceptable_airline = any(
        airline_status.get(code, False)
        for code in airline_codes
    )

    # If ALL airlines are unacceptable,
    # don't eliminate anything.
    if not has_acceptable_airline:
        return flights

    # Otherwise, keep only flights operated
    # by acceptable airlines.
    filtered_flights = []

    for flight in flights:
        
        airline_code = flight["airline"]["iata_code"]
        if airline_code == "ZZ":
            continue
        if airline_status.get(airline_code, False):
            filtered_flights.append(flight)
            
   
    

    return filtered_flights