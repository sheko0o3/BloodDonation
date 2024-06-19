from django.urls import path

from . import views


urlpatterns = [

    path(route="create/", view=views.SaveLoginInfo.as_view()),
    path(route="changepassword/", view=views.ChangePassword.as_view()),
    path(route="login/", view=views.Login.as_view())

    
]