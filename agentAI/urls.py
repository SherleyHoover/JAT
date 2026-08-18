from django.urls import path

from .views import AgentAPIView


urlpatterns = [

    path(
        "chat/",
        AgentAPIView.as_view()
    )

]