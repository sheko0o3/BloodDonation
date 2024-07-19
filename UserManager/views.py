import re
from tkinter import N
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password


from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import (IsAuthenticated, IsAdminUser)


from database import models
from SerializerApp.serializers import UserInformationSerializer, UserSerializer

from oauth2_provider.contrib.rest_framework import (OAuth2Authentication,
                                                    TokenHasReadWriteScope)
from Permissions.permissions import (UpdateOwnInfo, SaveOwnInfo)




class SaveUserInformation(APIView):
    authentication_classes = (OAuth2Authentication,)
    permission_classes = (SaveOwnInfo, IsAuthenticated)
    
    
    def post(self, request):
        user = request.user
        self.check_object_permissions(request=request, obj=user)

        serializer = UserInformationSerializer(data=request.data)
        if serializer.is_valid():
            user_info= models.UserInformation.objects.create(
                # user = User.objects.get(id=request.data["user"]),
                user = user,
                bloodType = models.BloodType.objects.get(bloodtype=request.data["bloodType"]),
                name = request.data["name"],
                mobile = request.data["mobile"],
                govern = models.Govern.objects.get(name=request.data["govern"]),
                state = models.GovernState.objects.get(name=request.data["state"]),
                Card_number = request.data["Card_number"],
                date_of_donation = request.data["date_of_donation"],
                age = request.data["age"],
                gender = request.data["gender"]
            )
            
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

class UpdateInformation(APIView):
    authentication_classes = (OAuth2Authentication,)
    permission_classes = (UpdateOwnInfo, IsAuthenticated)
    
    def get_user(self,request):
        try:
            # user = User.objects.get(id=request.data["user"])
            user = request.user
            self.check_object_permissions(request=request, obj=user)
            user_info = models.UserInformation.objects.get(user=user)
            return user_info

        except ObjectDoesNotExist:

            raise Http404
            

    def get(self, request):
        
        user_info = self.get_user(request=request)
        serializer = UserInformationSerializer(instance=user_info, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
        


    def put(self, request):
        # try:
        #     user = User.objects.get(id=request.data["user"])
        #     user_info = models.UserInformation.objects.get(user=user)
        # except ObjectDoesNotExist:
        #     return Response(data={"message": "NOT FOUND!"}, status=status.HTTP_404_NOT_FOUND)
        user_info = self.get_user(request=request)

        if user_info.user.check_password(request.data.get("password", None)):
            serializer = UserInformationSerializer(instance=user_info, data=request.data)
            if serializer.is_valid():
                serializer.save(password=make_password(request.data("password", None)))
                serializer.help_text = "Update Success"
                return Response(data={"message": serializer.help_text}, status=status.HTTP_202_ACCEPTED)
            return Response(data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(data={"message": "Wrong Password!"}, status=status.HTTP_401_UNAUTHORIZED)
    


        
class DeleteUser(APIView):
    authentication_classes = (OAuth2Authentication,)
    permission_classes = (SaveOwnInfo, IsAuthenticated)

    def get_user(self,request):
        try:
            # user = User.objects.get(id=request.data.get("user", None))
            user = request.user
            self.check_object_permissions(request=request, obj=user)
            return user
        except ObjectDoesNotExist:

            raise Http404
            

    def delete(self, request):
        
        user = self.get_user(request=request)
        
        if user.check_password(request.data.get("password", None)):
            user.delete()
            return Response(data={"messgae": "Account Deleted"}, status=status.HTTP_204_NO_CONTENT)
        return Response(data={"message":"Wrong Password!"}, status=status.HTTP_204_NO_CONTENT)
