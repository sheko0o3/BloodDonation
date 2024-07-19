from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password


from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


from database import models
from SerializerApp.serializers import UserInformationSerializer, UserSerializer
from FiltersApp.filters import SearchDonatorFilter

from oauth2_provider.contrib.rest_framework import (OAuth2Authentication)


class ShowDonatorInfo(APIView):
    authentication_classes = (OAuth2Authentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            self.check_object_permissions(request=request, obj=request.user)
            user_info = models.UserInformation.objects.get(user=user)
            return user_info

        except ObjectDoesNotExist:
            raise Http404


    def get(self,request):
        user = self.get_object(request=request ,pk=request.data["user_id"])
        serializer = UserInformationSerializer(instance=user, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)



class SearchDonator(APIView):
    authentication_classes = (OAuth2Authentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        self.check_object_permissions(request=request, obj=request.user)
        queryset = models.UserInformation.objects.all().order_by("id")
        filterset = SearchDonatorFilter(data=request.GET, queryset=queryset)
        serializer = UserInformationSerializer(instance=filterset.qs, many=True)
        return Response(data={"Donators":serializer.data}, status=status.HTTP_200_OK)
    


class AnonymousUser(APIView):

    def get(self, request):

        queryset = models.UserInformation.objects.all()
        serializer = UserInformationSerializer(instance=queryset, many=True)
        for item in serializer.data:
            item["mobile"] = "Please Log In to Show"
        return Response(data={"data":serializer.data}, status=status.HTTP_200_OK)
                                

class Donators(APIView):

    authentication_classes = (OAuth2Authentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        self.check_object_permissions(request=request, obj=request.user)
        queryset = models.UserInformation.objects.all()
        serializer = UserInformationSerializer(instance=queryset, many=True) 
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    

class ResetData(APIView):
    pass


