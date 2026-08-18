import os

from openai import OpenAI
from dotenv import load_dotenv
from .base import BaseLLM

load_dotenv()


class DeepSeekLLM(BaseLLM):

    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"
        )
    def generate(self, prompt):
        return super().generate(prompt)
    def analyze_request(self, user_request):

        print("Calling DeepSeek for travel intent...")

        response = self.client.chat.completions.create(
            model="deepseek-chat",

            messages=[
                {
                    "role": "system",
                    "content": """
You are a travel request analysis agent.

Your job is to analyze a user's natural-language flight request.

You MUST extract:

1. The departure city.
2. The arrival city.
3. Whether the user expresses a preference concerning:
   - price
   - layover
   - total travel time

You must NOT determine airports.

For example, if the user says:
"I want to fly from Hong Kong to New York"

you should return:

{
    "origin_city": "Hong Kong",
    "destination_city": "New York"
}

Do NOT return airport codes.

The airport database will be used later by the program
to determine which airports belong to those cities.
CITY NAME INTERPRETATION:

The user may use:
- abbreviations
- common short names
- airport-related city names
- informal names
- common English abbreviations

You should interpret common geographic abbreviations when their meaning
is unambiguous.

Examples:
- LA → Los Angeles
- NYC → New York
- SF → San Francisco
- DC → Washington, D.C.
- HK → Hong Kong
- Shanghai → Shanghai
- Tokyo → Tokyo

However, do not invent a location when an abbreviation is ambiguous.

The returned origin_city and destination_city should contain the
standard city name that can be matched against the provided airport
database.
========================================
DEFAULT SCORING
========================================

If the user does not express any preference, use:

price: 50
layover: 30
total_time: 20

========================================
USER PREFERENCES
========================================

If the user expresses preferences, modify the weights
according to the meaning of the request.

The three weights MUST:

- be integers
- be between 0 and 100
- add up to exactly 100

The weights represent:

price:
How important low price is.

layover:
How important a good layover is.

total_time:
How important a short overall travel time is.

Examples:

"I want the cheapest flight possible."

should strongly prioritize price.

"I don't care about price, I just want to get there quickly."

should strongly prioritize total travel time.

"I hate long layovers."

should strongly prioritize layover quality.

If the user does not mention a category,
use the default weighting unless the user's statement
clearly implies that the category should receive less weight.

========================================
OUTPUT
========================================

Return ONLY valid JSON.

Use exactly this structure:

{
    "origin_city": "string",
    "destination_city": "string",

    "preferences": {
        "price": {
            "mentioned": true,
            "weight": 50
        },

        "layover": {
            "mentioned": false,
            "weight": 30
        },

        "total_time": {
            "mentioned": true,
            "weight": 20
        }
    }
}

"mentioned" means that the user explicitly expressed
a preference concerning that category.

Do not invent cities.

If you cannot determine the departure or arrival city,
return null for that field. Be noted that Fenway, New Carthage, Nebula City, New Tyre, Warren City, Romney are cities.

The weights must always add up to 100.
"""
                },
                {
                    "role": "user",
                    "content": user_request
                }
            ]
        )

        print("DeepSeek has finished analyzing travel request")

        result = response.choices[0].message.content

        print(result)

        return result