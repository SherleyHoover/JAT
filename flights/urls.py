from django.urls import path

from .views import (FlightListAPIView, FlightSearchAPIView, newFlightSearchAPIView,search_flights, test_travel_intent) 




urlpatterns = [

    path(
        "flights/",
        FlightListAPIView.as_view()
    ),
    
    
    path(
        "flights/search/",
        FlightSearchAPIView.as_view()
    ),
    
    path(
        "flights/search/new/",
        newFlightSearchAPIView.as_view()
    ),
    path(
        "flights/test/",
        search_flights
    ),
    path(
        "test/travel-intent/",
        test_travel_intent
    )
    
]