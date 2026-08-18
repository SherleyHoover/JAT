import requests
import os
from .base import FlightProvider
from dotenv import load_dotenv
import time
from django.conf import settings
from .duffel_convert import normalize_duffel_offer
load_dotenv()

class DuffelFlightProvider(FlightProvider):

    def search(self, request):

        response = requests.post(
            "https://api.duffel.com/air/offer_requests",
            headers={
                "Authorization": f"Bearer {settings.DUFFEL_ACCESS_TOKEN}",
                "Content-Type": "application/json",
                "Duffel-Version": "v2",
            },
            json={
                "data": {
                    "slices": [
                        {
                            "origin": request["origin"],
                            "destination": request["destination"],
                            "departure_date": request["departure_date"],
                        }
                    ],
                    "passengers": [
                        {
                            "type": "adult"
                        }
                    ],
                    "cabin_class": "economy",
                }
            },
        )
        
       #time.sleep(3)
        print(
    "TOKEN:",
    os.getenv("DUFFEL_ACCESS_TOKEN")
)       
        print(request)
        response.raise_for_status()
        data = response.json()
        offers = data.get("data", {}).get("offers", [])
        if not response:
            print("!!!!!!!!!!")
        #print(response.json())
        for offer in offers:
         segment = offer["slices"][0]["segments"][0]

        
        return [
    normalize_duffel_offer(offer)
    for offer in offers
]