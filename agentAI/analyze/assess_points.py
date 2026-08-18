from datetime import datetime, timedelta


MIN_LAYOVER = timedelta(hours=2, minutes=0)
IDEAL_LAYOVER = timedelta(hours=3)

MAX_LAYOVER_SCORE = 30
MAX_PRICE_SCORE = 50


def parse_time(time_string):
    return datetime.fromisoformat(
        time_string.replace("Z", "+00:00")
    )


def calculate_layovers(flight):
    """
    Return all layovers for a flight.

    Example:
        segment 1 arrives at 12:00
        segment 2 departs at 14:00

        layover = 2 hours
    """

    segments = flight["segments"]

    layovers = []

    for i in range(len(segments) - 1):

        arrival_time = parse_time(
            segments[i]["arrival_time"]
        )

        departure_time = parse_time(
            segments[i + 1]["departure_time"]
        )

        layover = departure_time - arrival_time

        layovers.append(layover)

    return layovers


def eliminate_short_layovers(flights):
    """
    Remove any flight containing a layover shorter
    than 2 hours 30 minutes.

    Exactly 2h30m is allowed.
    """

    remaining = []

    for flight in flights:

        layovers = calculate_layovers(flight)

        invalid = False

        for layover in layovers:

            if layover < MIN_LAYOVER:
                invalid = True
                break

        if not invalid:
            remaining.append(flight)

    return remaining


def calculate_layover_score(flight):
    """
    Maximum = 30 points.

    Exactly 3h = 30 points.

    Every 30-minute interval away from 3h
    subtracts 2 points.

    If a flight has multiple layovers, the score
    is based on the total deviation from the ideal
    across all layovers.
    """

    layovers = calculate_layovers(flight)

    # Non-stop flight
    if not layovers:
        return 30

    total_score = 0

    for layover in layovers:

        difference = abs(
            layover - IDEAL_LAYOVER
        )

        intervals = difference.total_seconds() / (
            30 * 60
        )

        score = max(
            0,
            30 - int(intervals) * 2
        )

        total_score += score

    # Average the scores if there are multiple layovers
    return round(total_score / len(layovers))


def calculate_price_scores(flights):

    if not flights:
        return flights

    min_price = min(
        flight["price"]
        for flight in flights
    )

    base = min_price * 0.10

    for flight in flights:

        price = flight["price"]

        if base == 0:

            score = 50

        else:

            n = int(
                (price - min_price) // base
            )

            if n <= 1:

                score = 50

            else:

                score = max(
                    0,
                    50 - (n - 1) * 5
                )

        # Put the score directly onto the flight
        flight["price_score"] = score

    return flights

def calculate_time_scores(flights):
    for flight in flights:
        flight["time_score"] = 20
        
        
        
def summarize_flights(flights):

    # 1. Eliminate flights with short layovers
    flights = eliminate_short_layovers(flights)

    # 2. Calculate layover scores
    for flight in flights:
        flight["layover_score"] = calculate_layover_score(
            flight
        )

    # 3. Calculate price scores
    flights = calculate_price_scores(flights)

        
    for flight in flights:

        flight["final_score"] = (
            flight["price_score"]
            + flight["layover_score"]
            #+ flight["time_score"]
        )
        
    flights.sort(
        key=lambda flight: flight["final_score"],
        reverse=True
    )
    i = 0
    for flight in flights:
        flight["id"] = i
        i = i + 1
    return flights