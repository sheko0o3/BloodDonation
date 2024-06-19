from django.urls import path


from . import views



urlpatterns = [
    path(route="profileinfo/", view=views.ShowDonatorInfo.as_view()),
    path(route="search/", view=views.SearchDonator.as_view()),
    path(route="anonymous/", view=views.AnonymousUser.as_view()),
    path(route="donators/", view=views.Donators.as_view())
    
]