from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView



from SerializerApp.serializers import (UserSerializer, ChangePasswordSerializer, 
                                       UserInformationSerializer)
from database import models



class SaveLoginInfo(APIView):

    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)

        if serializer.is_valid():
            serializer.save(password=make_password(data["password"]))
            return Response(data={"message":"Account Created"}, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)




class ChangePassword(APIView):
    
    def put(self, request):
        user = User.objects.get(id=request.data["user_id"]) 
        serializer = ChangePasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                password_validation.validate_password(password=serializer.data["new_password"])
                
            except ValidationError:
                msg = password_validation.password_validators_help_texts()
                return Response(data={"msg":"Password Not Valid",
                                      "requirements": msg}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                old_password = serializer.data["old_password"]
                if not user.check_password(old_password):
                    return Response(data={"message":"Wrong Password"})
                else:
                    new_password = serializer.data["new_password"]
                    confirm_password = serializer.data["confirm_password"]
                    if new_password == old_password:
                        return Response(data={"message":"U Entered Old Password"})
                    elif new_password != confirm_password:
                        return Response(data={"message":"Wrong Confirm Password"})
                    else:
                        user.set_password(new_password)
                        user.save()
                        return Response(data={"message":"Password Updated"})

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)    




class Login(APIView):
    
     def get(self, request):
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
                                      "data":serializer.data})
            return Response(data={"msg":"Wrong Password"})
        