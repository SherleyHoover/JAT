from .base import BaseLLM
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)



class GeminiLLM(BaseLLM):

    def generate(self, prompt):

        print(
            "Calling Gemini..."
        )

        return """
        {
            "tool": "search_flights",
            "arguments": {
                "origin": "FNY",
                "destination": "NTP"
            }
        }
        """