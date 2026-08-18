from .gemini import GeminiLLM
from .deepseek import DeepSeekLLM



class LLMRouter:


    def __init__(self):

        self.models = [

            GeminiLLM(),

            DeepSeekLLM()

        ]



    def generate(self, prompt):

        for model in self.models:

            try:

                return model.generate(
                    prompt
                )


            except Exception:

                continue



        raise Exception(
            "All LLMs failed"
        )