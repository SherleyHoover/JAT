from rest_framework import serializers

from .models import (
    Airline,
    Airport,
    Flight,
    Segment,
    Aircraft
)
class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = "__all__"


class AirlineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Airline
        fields = "__all__"



class AirportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Airport
        fields = "__all__"



class SegmentSerializer(serializers.ModelSerializer):
    departure_airport = AirportSerializer()
    arrival_airport = AirportSerializer()
    class Meta:
        model = Segment
        fields = "__all__"



class FlightSerializer(serializers.ModelSerializer):
    airline = AirlineSerializer()
    segments = SegmentSerializer(many=True)
    aircraft = AircraftSerializer()
    class Meta:
        model = Flight
        fields = "__all__"