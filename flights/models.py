from django.db import models


class Airline(models.Model):
    name = models.CharField(max_length=100)
    iata_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    rating = models.FloatField()

    def __str__(self):
        return self.name
    
class Airport(models.Model):
    name = models.CharField(max_length=100)
    iata_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Aircraft(models.Model):

    model = models.CharField(
        max_length=100
    )

    manufacturer = models.CharField(
        max_length=100
    )

    seats = models.IntegerField()


    def __str__(self):
        return self.model


class Flight(models.Model):
    flight_number = models.CharField(max_length=10)
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    currency = models.CharField(max_length=5, default='USD')
    price = models.FloatField()
    aircraft = models.ForeignKey(
    Aircraft,
    null=True,
    blank=True,
    on_delete=models.SET_NULL
)
    
    def __str__(self):
        return self.flight_number
    
class Segment(models.Model):
    flight = models.ForeignKey(
        Flight,
        related_name="segments",
        on_delete=models.CASCADE
    )
    departure_airport = models.ForeignKey(
        Airport,
        related_name="departures",
        on_delete=models.CASCADE
    )
    arrival_airport = models.ForeignKey(
        Airport,
        related_name="arrivals",
        on_delete=models.CASCADE
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    

    def __str__(self):
        return f"{self.departure_airport}-{self.arrival_airport}"
    
class Route(models.Model):

    origin = models.ForeignKey(
        Airport,
        related_name="routes_from",
        on_delete=models.CASCADE
    )


    destination = models.ForeignKey(
        Airport,
        related_name="routes_to",
        on_delete=models.CASCADE
    )


    def __str__(self):
        return (
            f"{self.origin}"
            "-"
            f"{self.destination}"
        )
        
class FlightSchedule(models.Model):

    flight_number = models.CharField(
        max_length=20
    )
    airline = models.ForeignKey(
        Airline,
        on_delete=models.CASCADE
    )
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE
    )
    departure_time = models.TimeField()
    operating_days = models.CharField(
        max_length=50
    )
    def __str__(self):

        return self.flight_number


class Airport_Data(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    iata_code = models.CharField(
        max_length=3,
        unique=True
    )

    def __str__(self):
        return f"{self.name} ({self.iata_code})"
    
    
class Airline_Data(models.Model):
    name = models.CharField(max_length= 200)
    iata_code = models.CharField(
        max_length=3,
        unique=True
    )
    country = models.CharField(max_length=100)
    region_acceptable = models.BooleanField(default=False)
    def __str__(self):
            return f"{self.name} ({self.iata_code})"
    
# Create your models here.
