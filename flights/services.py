from .providers.fictional import (
    FictionalFlightProvider
)

from .providers.duffel import (
    DuffelFlightProvider
)


class FlightSearchService:


    def __init__(self):

        self.providers = [
            FictionalFlightProvider(),
            DuffelFlightProvider()
        ]


    def search(self, request):

        results = []
        origin = request["origin"]
        destination = request["destination"]
        departure_date = request["departure_date"]

        for provider in self.providers:

            try:
                flights = provider.search(request)

                results.append(flights)

            except Exception as e:
                print(
                    f"{provider.__class__.__name__} failed: {e}"
                )

         
        return results
    
    
    #So, bye, bye, Miss American Pie. Drove my chevy to the levy but the levy was dry.
    #So, bye, bye, Miss American Pie. Drove my chevy to the levy but the levy was dry.
    #So, bye, bye, Miss American Pie. Drove my chevy to the levy but the levy was dry.