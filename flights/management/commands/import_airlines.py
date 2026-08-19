import csv

from django.core.management.base import BaseCommand
from flights.models import Airline_Data


class Command(BaseCommand):
    help = "Import active airlines from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_file",
            help="Path to the airlines CSV file"
        )

    def handle(self, *args, **options):
        csv_file = options["csv_file"]

        created_count = 0
        updated_count = 0
        skipped_inactive = 0
        skipped_no_iata = 0

        with open(csv_file, "r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:

                # Only import active airlines
                if row["Active"].strip().upper() != "Y":
                    skipped_inactive += 1
                    continue

                iata_code = row["IATA"].strip()

                # Skip airlines without an IATA code
                if not iata_code:
                    skipped_no_iata += 1
                    continue

                name = row["Name"].strip()
                country = row["Country"].strip()

                airline, created = Airline_Data.objects.update_or_create(
                    iata_code=iata_code,
                    defaults={
                        "name": name,
                        "country": country,
                    },
                )

                if created:
                    created_count += 1
                else:
                    updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Airline import complete: "
                f"{created_count} created, "
                f"{updated_count} updated, "
                f"{skipped_inactive} inactive skipped, "
                f"{skipped_no_iata} without IATA skipped."
            )
        )