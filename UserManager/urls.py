from django.urls import path


from . import views


urlpatterns = [
    path(route="saveinfo/", view=views.SaveUserInformation.as_view()),
    path(route="updateinfo/", view=views.UpdateInformation.as_view()),
    path(route="deleteuser/", view=views.DeleteUser.as_view()),
]