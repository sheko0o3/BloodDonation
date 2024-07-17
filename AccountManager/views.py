from tkinter import N
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework.permissions import IsAuthenticated



from Permissions.permissions import (UpdateOwnInfo,UpdateOwnPassword)
from SerializerApp.serializers import (UserSerializer, ChangePasswordSerializer, 
                                       UserInformationSerializer)
from database import models

import os
import requests

class SaveLoginInfo(APIView):

    def create_token(self, name, password):

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
    
    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)

        name = data.get("username", None)
        password = data.get("password", None)

        if serializer.is_valid():
            
            try:
                password_validation.validate_password(password=password)
                    
            except ValidationError:
                msg = password_validation.password_validators_help_texts()
                
                return Response(data={"msg":"Password Not Valid",
                                    "requirements": msg}, status=status.HTTP_406_NOT_ACCEPTABLE)
            
            serializer.save(password=make_password(data["password"]))
            token = self.create_token(name=name, password=password)
            return Response(data={"message":"Account Created"}, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)




class ChangePassword(APIView):

    permission_classes = (UpdateOwnPassword,)
    
    def put(self, request):
        try:
            user = User.objects.get(id=request.data["user_id"])
        except ObjectDoesNotExist:
            return Response(data={"error": "Not Found"})     
        serializer = ChangePasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            old_password = serializer.data["old_password"]
            new_password = serializer.data["new_password"]
            confirm_password = serializer.data["confirm_password"]

            if not user.check_password(old_password):
                return Response(data={"message":"Wrong Password"})
            else:
                try:
                    password_validation.validate_password(password=serializer.data["new_password"])
                    
                except ValidationError:
                    msg = password_validation.password_validators_help_texts()
                    return Response(data={"msg":"New Password Not Valid",
                                        "requirements": msg}, status=status.HTTP_406_NOT_ACCEPTABLE)
                else:
                    
                    if new_password == old_password:
                        return Response(data={"message":"New Password Can't be Old Password"})
                    elif new_password != confirm_password:
                        return Response(data={"message":"Wrong Confirm Password"})
                    else:
                        user.set_password(new_password)
                        user.save()
                        return Response(data={"message":"Password Updated"})

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)    




class Login(APIView):
    
    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return Response(data={"msg":"Not found"})
        else:
            if user.check_password(password):
                users = models.UserInformation.objects.all()
                serializer = UserInformationSerializer(instance=users, many=True)
                return Response(data={"msg":"Logged In",
                                        "user_id":user.id,
                                        "data":serializer.data
                                        })
            return Response(data={"msg":"Wrong Password"})


