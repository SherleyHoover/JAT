from django.test import TestCase
from providers.duffel import DuffelFlightProvider
from dotenv import load_dotenv
import os
import json
load_dotenv()

print(os.getenv("DUFFEL_ACCESS_TOKEN"))

provider = DuffelFlightProvider()


request = {
    "origin": "PEK",
    "destination": "JFK",
    "departure_date": "2026-09-01"
}


results = provider.search(request)
i = 0
print(results)
for flight in results["data"][0]:
    i=i+1
    if i < 10:
        break
    print(flight)


# Create your tests here.
