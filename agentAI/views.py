from rest_framework.views import APIView
from rest_framework.response import Response

from .router import AgentRouter



class AgentAPIView(APIView):

    def get(self, request):

        message = request.GET.get(
            "message"
        )


        agent = AgentRouter()


        result = agent.run(
            message
        )


        return Response(
            {
                "result": result
            }
        )

# Create your views here.
