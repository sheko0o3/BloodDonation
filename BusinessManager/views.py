from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


from SerializerApp.serializers import (GovernSerializer,StatesSerializer,
                                       BloodTypesSerializer)
from database import models

from oauth2_provider.contrib.rest_framework import (OAuth2Authentication, TokenHasReadWriteScope)
from oauth2_provider.models import AccessToken


import os
import requests



class AllGoverns(APIView):
    authentication_classes = (OAuth2Authentication,)

    def get(self, request):
        queryset = models.Govern.objects.all().order_by("name")
        serializer = GovernSerializer(instance=queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    


class AllStates(APIView):

    def get(self, request):
        queryset = models.GovernState.objects.all().order_by("name")
        serializer = StatesSerializer(instance=queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    


class AllBloodTypes(APIView):

    def get(self, request):
        queryset = models.BloodType.objects.all()
        serializer = BloodTypesSerializer(instance=queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    


class Token(APIView):
    def create_token(self, name=None, password=None):

        body: dict = {
            "client_id":os.getenv("CLIENT_ID"),
            "client_secret":os.getenv("CLIENT_SECRET"),
            "username": name,
            "password": password,
            "grant_type":os.getenv("GRANT_TYPE")
        }

        response = requests.post(url="http://127.0.0.1:8000/o/token/", data=body)
        data = response.json()
        return data
    
    def get_user(self, request):
        try:
            user = User.objects.get(username=request.data["username"])
            return user
        except :
            raise Http404

    
    def get(self, request):
        user = self.get_user(request=request)
        if not user.check_password(raw_password=request.data.get("password", None)):
            return Response(data={"error":"Wrong Password"})
        else:
            try:
                token_exists = AccessToken.objects.get(user=user)
            except ObjectDoesNotExist:
                token = self.create_token(name=user.username, password=request.data.get("password", None))
                return Response(data={"message":"Token created!",
                                    "Token":token}, status=status.HTTP_200_OK)
        
            else:
                return Response(data={"Token":token_exists.token,
                                      "Scopes":token_exists.scopes,}, status=status.HTTP_200_OK)
        

        