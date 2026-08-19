from rest_framework import generics

from .models import Flight
from .models import Airport_Data
from .serializers import FlightSerializer

from rest_framework.response import Response
from rest_framework.views import APIView

from .services import FlightSearchService
from agentAI.llm.deepseek import DeepSeekLLM
from agentAI.flight_analyzer import FlightAnalyzer
from agentAI.new_flight_analyzer import newFlightAnalyzer
import json
from django.http import JsonResponse

class FlightListAPIView(
    generics.ListAPIView
):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
class newFlightSearchAPIView(APIView):
    def post(self, request):
        print(request)
        # =====================================
        # 1. Get user's natural-language request
        # =====================================
        user_text = request.data.get("query")
        departure_date = request.data.get(
            "departure_date"
        )
        print("========== USER REQUEST ==========")
        print(user_text)
        print("===================================")
        # =====================================
        # 2. Send request to DeepSeek
        # =====================================
        llm = DeepSeekLLM()

        llm_result = llm.analyze_request(
            user_text
        )

        # =====================================
        # 3. Convert JSON string → Python dict
        # =====================================

        try:

            intent = json.loads(
                llm_result
            )

        except json.JSONDecodeError:

            return JsonResponse(
                {
                    "error": "DeepSeek did not return valid JSON",
                    "raw": llm_result
                },
                status=500
            )

        # =====================================
        # 4. Extract cities
        # =====================================

        origin_city = intent.get(
            "origin_city"
        )

        destination_city = intent.get(
            "destination_city"
        )
        print("========== BEFORE AIRPORT DATABASE QUERY ==========")
        origin_airports = Airport_Data.objects.filter(
        city__iexact=origin_city
)

        destination_airports = Airport_Data.objects.filter(
        city__iexact=destination_city
)
        print("========== AFTER AIRPORT DATABASE QUERY ==========")
        # =====================================
        # 5. Extract weights
        # =====================================

        preferences = intent.get(
            "preferences",
            {}
        )

        weights = {

            "price":
            preferences
            .get("price", {})
            .get("weight", 50),

            "layover":
            preferences
            .get("layover", {})
            .get("weight", 30),

            "total_time":
            preferences
            .get("total_time", {})
            .get("weight", 20)

        }

        # =====================================
        # DEBUG
        # =====================================

        print("========== TRAVEL INTENT ==========")

        print(
            "Origin:",
            origin_city
        )

        print(
            "Destination:",
            destination_city
        )

        print(
            "Weights:",
            weights
        )

        print("===================================")

        # =====================================
        # Get All Available Airport IATA Codes
        # =====================================
        origin_codes = [
    airport.iata_code
    for airport in origin_airports
]

        destination_codes = [
    airport.iata_code
    for airport in destination_airports
]       
        print("Origin airports:", list(origin_airports.values("iata_code", "city")))
        print("Destination airports:", list(destination_airports.values("iata_code", "city")))
        print("Origin airport count:", origin_airports.count())
        print("Destination airport count:", destination_airports.count())
        #======================================
        #Generate All Available Pairs of Airports
        #======================================
        airport_pairs = []

        for origin in origin_codes:

           for destination in destination_codes:

               airport_pairs.append(
            {
                "origin": origin,
                "destination": destination
            }
        )
        
        
            
        service = FlightSearchService()
        all_flights = []
        for pair in airport_pairs:
            search_request = {
                "origin": pair["origin"],
                "destination": pair["destination"],
                "departure_date": departure_date
            }
            flights = service.search(search_request)
            fictional = flights[0]
            try: duffels = flights[1]
            except: duffels = []
       
            fictional_serializer = FlightSerializer(
               fictional,
                many=True
            )
            fictional_data = fictional_serializer.data
            flights = list(fictional_data) + duffels
            
            all_flights.extend(flights)
        analyzer = newFlightAnalyzer()
        analysis = analyzer.new_analyze(all_flights, weights)
        #print(analysis)
        return JsonResponse(
            {
                "analysis": analysis
            }
        )
        
        
        
        
        
        
class FlightSearchAPIView(APIView):

    def post(self, request):
        print(request)
        
        search_request = {

            "origin":
            request.data.get("origin"),

            "destination":
            request.data.get("destination"),

            "departure_date":
            request.data.get("departure_date")

        }


        service = FlightSearchService()


        flights = service.search(
            search_request
        )
        
        fictional = flights[0]
        try: duffels = flights[1]
        except: duffels = []
       
        fictional_serializer = FlightSerializer(
    fictional,
    many=True
)

        fictional_data = fictional_serializer.data

        all_flights = list(fictional_data) + duffels
        print("========== ALL FLIGHTS ==========")

        #for flight in all_flights:
         #print(flight)

        print("=================================")
        analyzer = FlightAnalyzer()
        print("analyzed")
        analysis = analyzer.analyze(all_flights)
        
        try: fictional = FlightSerializer(
                    fictional,
                    many=True
                )
        except: fictional
        print("View sent")
        return JsonResponse(
    {   "analysis": analysis,
        
    },
    safe=False
)
        try: serializer = FlightSerializer(
            flights,
            many=True
        )
        except Exception as e: 
            serializer = serializer
            return JsonResponse(
                    serializer,
                    safe=False
                )

        return Response(
            serializer.data
        )
        
        
from django.http import JsonResponse
import json

from .services import FlightSearchService


def search_flights(request):

    
    data = {
        "origin": "LAX",
        "destination": "BOS",
        "departure_date": "2026-08-20"
    }
    service = FlightSearchService()

    results = service.search(data)
   # print(results)
    return JsonResponse(
        results,
        safe=False
    )
    
from django.http import JsonResponse
from agentAI.llm.deepseek import DeepSeekLLM
import json


def test_travel_intent(request):

    llm = DeepSeekLLM()

    user_request = """
    I want to fly from Hong Kong to Boston.
    I don't really care about the price.
    I want to get there as quickly as possible,
    but I also don't want a ridiculously long layover.
    """

    result = llm.analyze_request(user_request)

    try:
        result = json.loads(result)
    except json.JSONDecodeError:
        return JsonResponse(
            {
                "error": "LLM did not return valid JSON",
                "raw": result
            },
            status=500
        )

    return JsonResponse(result)