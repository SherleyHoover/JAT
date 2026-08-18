import json

from .llm.router import LLMRouter
from .tools import search_flights
from .prompts import SYSTEM_PROMPT



class AgentRouter:


    def __init__(self):

        self.llm = LLMRouter()



    def run(self, user_message):


        prompt = (
            SYSTEM_PROMPT
            +
            "\nUser:"
            +
            user_message
        )


        response = self.llm.generate(
            prompt
        )


        try:

         action = json.loads(response)

        except json.JSONDecodeError:

          return {
        "error": "LLM returned invalid JSON",
        "raw_response": response
    }


        if action["tool"] == "search_flights":

            args = action["arguments"]


            return search_flights(
                **args
            )