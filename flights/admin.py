from django.contrib import admin
from .models import Airline, Airport, Flight, Segment, Aircraft, Route, FlightSchedule, Airport_Data, Airline_Data

class AirportAdmin(admin.ModelAdmin):
    search_fields = ["city"]

admin.site.register(Airline)
admin.site.register(Airport)
admin.site.register(Flight)
admin.site.register(Segment)
admin.site.register(Aircraft)
admin.site.register(Route)
admin.site.register(FlightSchedule)
admin.site.register(Airport_Data, AirportAdmin)
admin.site.register(Airline_Data)


# Register your models here.
