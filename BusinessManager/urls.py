from django.urls import path

from . import views

urlpatterns = [
    path("governs/", view=views.AllGoverns.as_view()),
    path("states/", view=views.AllStates.as_view()),
    path("bloodtypes/", view=views.AllBloodTypes.as_view()),
    path("token/", view=views.Token.as_view()),
]