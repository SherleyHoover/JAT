from datetime import datetime, timedelta


MIN_LAYOVER = timedelta(
    hours=2,
    minutes=30
)

IDEAL_LAYOVER = timedelta(
    hours=3
)


# Original scoring model
BASE_PRICE_POINTS = 50
BASE_LAYOVER_POINTS = 30
BASE_TIME_POINTS = 20


def parse_time(time_string):

    return datetime.fromisoformat(
        time_string.replace("Z", "+00:00")
    )


# ============================================================
# LAYOVERS
# ============================================================

def calculate_layovers(flight):

    segments = flight["segments"]

    layovers = []

    for i in range(
        len(segments) - 1
    ):

        arrival_time = parse_time(
            segments[i]["arrival_time"]
        )

        departure_time = parse_time(
            segments[i + 1]["departure_time"]
        )

        layover = (
            departure_time
            - arrival_time
        )

        layovers.append(
            layover
        )

    return layovers


def eliminate_short_layovers(flights):

    remaining = []

    for flight in flights:

        layovers = calculate_layovers(
            flight
        )

        invalid = False

        for layover in layovers:

            if layover < MIN_LAYOVER:

                invalid = True
                break

        if not invalid:

            remaining.append(
                flight
            )

    return remaining


# ============================================================
# LAYOVER SCORE
# ============================================================

def calculate_layover_score(flight):

    layovers = calculate_layovers(
        flight
    )

    # Non-stop flight
    if not layovers:
        return BASE_LAYOVER_POINTS


    scores = []

    for layover in layovers:

        difference = abs(
            layover
            - IDEAL_LAYOVER
        )

        intervals = int(
            difference.total_seconds()
            // (30 * 60)
        )

        score = max(
            0,
            BASE_LAYOVER_POINTS
            - intervals * 2
        )

        scores.append(
            score
        )


    # Multiple layovers:
    # use their average
    return round(
        sum(scores) / len(scores)
    )


# ============================================================
# PRICE SCORE
# ============================================================

def calculate_price_scores(flights):

    if not flights:
        return flights


    min_price = min(
        flight["price"]
        for flight in flights
    )

    base = (
        min_price * 0.10
    )


    for flight in flights:

        price = flight["price"]


        if base == 0:

            score = BASE_PRICE_POINTS

        else:

            n = int(
                (price - min_price)
                // base
            )

            if n <= 1:

                score = BASE_PRICE_POINTS

            else:

                score = max(
                    0,
                    BASE_PRICE_POINTS
                    - (n - 1) * 5
                )


        flight["price_score_raw"] = score


    return flights


# ============================================================
# TOTAL TRAVEL TIME
# ============================================================

def calculate_total_time(
    flight
):

    segments = flight["segments"]


    departure = parse_time(
        segments[0]["departure_time"]
    )

    arrival = parse_time(
        segments[-1]["arrival_time"]
    )


    return arrival - departure


def calculate_time_scores(
    flights
):

    if not flights:
        return flights


    # Find shortest overall travel time

    min_time = min(
        calculate_total_time(flight)
        for flight in flights
    )


    for flight in flights:

        total_time = calculate_total_time(
            flight
        )


        # How much longer than the
        # shortest flight?

        extension = (
            total_time - min_time
        )


        # Number of complete 10% intervals

        ten_percent = (
            min_time.total_seconds()
            * 0.10
        )


        if ten_percent == 0:

            score = BASE_TIME_POINTS

        else:

            n = int(
                extension.total_seconds()
                // ten_percent
            )


            # Every 10% extension
            # loses 10% of the points.
            #
            # 20 points
            # 10% = 2 points
            #
            # n = 0 → 20
            # n = 1 → 18
            # n = 2 → 16
            # etc.

            score = max(
                0,
                BASE_TIME_POINTS
                - n * 2
            )


        flight["time_score_raw"] = score


    return flights


# ============================================================
# APPLY USER WEIGHTS
# ============================================================

def apply_weights(
    flights,
    weights
):

    price_weight = weights.get(
        "price",
        50
    )

    layover_weight = weights.get(
        "layover",
        30
    )

    time_weight = weights.get(
        "total_time",
        20
    )


    for flight in flights:

        # Scale original 50-point
        # price score to user's weight

        flight["price_score"] = round(
            flight["price_score_raw"]
            / BASE_PRICE_POINTS
            * price_weight,
            2
        )


        # Scale original 30-point
        # layover score to user's weight

        flight["layover_score"] = round(
            flight["layover_score"]
            / BASE_LAYOVER_POINTS
            * layover_weight,
            2
        )


        # Scale original 20-point
        # time score to user's weight

        flight["time_score"] = round(
            flight["time_score_raw"]
            / BASE_TIME_POINTS
            * time_weight,
            2
        )


        flight["final_score"] = round(
            flight["price_score"]
            + flight["layover_score"]
            + flight["time_score"],
            2
        )


    return flights


# ============================================================
# MAIN FUNCTION
# ============================================================

def summarize_flights(
    flights,
    weights=None
):

    if weights is None:

        weights = {
            "price": 50,
            "layover": 30,
            "total_time": 20
        }


    # --------------------------------
    # 1. Eliminate bad layovers
    # --------------------------------

    flights = eliminate_short_layovers(
        flights
    )


    # --------------------------------
    # 2. Calculate raw layover scores
    # --------------------------------

    for flight in flights:

        flight["layover_score"] = (
            calculate_layover_score(
                flight
            )
        )


    # --------------------------------
    # 3. Calculate raw price scores
    # --------------------------------

    flights = calculate_price_scores(
        flights
    )


    # --------------------------------
    # 4. Calculate raw total-time scores
    # --------------------------------

    flights = calculate_time_scores(
        flights
    )


    # --------------------------------
    # 5. Apply user's weights
    # --------------------------------

    flights = apply_weights(
        flights,
        weights
    )


    # --------------------------------
    # 6. Sort
    # --------------------------------

    flights.sort(
        key=lambda flight:
            flight["final_score"],
        reverse=True
    )


    return flights