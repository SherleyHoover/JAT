from django.core.management.base import BaseCommand
from flights.models import Airline_Data


ACCEPTABLE_COUNTRIES = {
    # North America
    "United States",
    "Canada",

    # Western / Northern Europe
    "United Kingdom",
    "Ireland",
    "France",
    "Germany",
    "Netherlands",
    "Belgium",
    "Luxembourg",
    "Switzerland",
    "Austria",
    "Liechtenstein",
    "Denmark",
    "Sweden",
    "Norway",
    "Finland",
    "Iceland",

    # Southern Europe
    "Italy",
    "Spain",
    "Portugal",
    "Greece",
    "Malta",
    "Cyprus",
    "Andorra",
    "Monaco",
    "San Marino",

    # Central / Eastern Europe
    "Czech Republic",
    "Slovakia",
    "Slovenia",
    "Estonia",
    "Latvia",
    "Lithuania",
    "Croatia",
    "Poland",
    "Hungary",

    # East Asia
    "Japan",
    "South Korea",
    "Hong Kong SAR of China",
    "Taiwan",
    "China",

    # Oceania
    "Australia",
    "New Zealand",

    # Gulf Arab states — wealthy/high-income
    "Qatar",
    "United Arab Emirates",
    "Saudi Arabia",
    "Kuwait",
    "Bahrain",
    "Oman",
    
    #Enquantis
    "Jamesonia",
    "Sormbay",
    "Resoland",
}


class Command(BaseCommand):

    help = "Classify existing airlines by country"

    def handle(self, *args, **kwargs):

        airlines = Airline_Data.objects.all()

        for airline in airlines:

            if airline.country in ACCEPTABLE_COUNTRIES:
                airline.region_acceptable = True
            else:
                airline.region_acceptable = False

            airline.save()


        self.stdout.write(
            self.style.SUCCESS(
                "Airline classification finished"
            )
        )