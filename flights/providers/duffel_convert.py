def normalize_duffel_offer(offer):
    """
    Convert Duffel offer format into internal flight format
    """

    # Use the first slice (for now)
    slice_data = offer["slices"][0]

    # Use first segment to get airline and flight number
    first_segment = slice_data["segments"][0]

    carrier = first_segment["marketing_carrier"]


    # Convert segments
    segments = []

    for index, segment in enumerate(slice_data["segments"]):

        segments.append(
            {
                "id": None,

                "departure_airport": {
                    "id": None,
                    "name": segment["origin"]["name"],
                    "iata_code": segment["origin"]["iata_code"],
                    "city": segment["origin"].get("city_name"),
                    "country": segment["origin"].get("iata_country_code"),
                },

                "arrival_airport": {
                    "id": None,
                    "name": segment["destination"]["name"],
                    "iata_code": segment["destination"]["iata_code"],
                    "city": segment["destination"].get("city_name"),
                    "country": segment["destination"].get("iata_country_code"),
                },

                "departure_time": segment["departing_at"],
                "arrival_time": segment["arriving_at"],

                # no database Flight object exists
                "flight": None
            }
        )


    return {

        # Duffel does not have your database ID
        "id": None,


        "airline": {
            "id": None,
            "name": carrier["name"],
            "iata_code": carrier["iata_code"],
            "country": None,
            "rating": None,
        },


        "segments": segments,


        "aircraft": {
            "id": None,
            "model": (
                first_segment["aircraft"]["name"]
                if first_segment.get("aircraft")
                else None
            ),
            "manufacturer": None,
            "seats": None,
        },


        "flight_number": (
            first_segment["marketing_carrier_flight_number"]
        ),


        "currency": offer["total_currency"],


        "price": float(
            offer["total_amount"]
        )
    }