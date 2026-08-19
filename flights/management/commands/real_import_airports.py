import csv

from django.core.management.base import BaseCommand
from flights.models import Airport_Data


class Command(BaseCommand):
    help = "Import airports with IATA codes from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_file",
            help="Path to the airports CSV file"
        )

    def handle(self, *args, **options):
        csv_file = options["csv_file"]

        created_count = 0
        updated_count = 0
        skipped_no_iata = 0

        with open(csv_file, "r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:

                # Only import airports with an IATA code
                iata_code = row["iata_code"].strip()

                if not iata_code:
                    skipped_no_iata += 1
                    continue

                name = row["name"].strip()
                city = row["municipality"].strip()
                country = row["iso_country"].strip()

                airport, created = Airport_Data.objects.update_or_create(
                    iata_code=iata_code,
                    defaults={
                        "name": name,
                        "city": city,
                        "country": country,
                    },
                )

                if created:
                    created_count += 1
                else:
                    updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Airport import complete: "
                f"{created_count} created, "
                f"{updated_count} updated, "
                f"{skipped_no_iata} without IATA skipped."
            )
        )