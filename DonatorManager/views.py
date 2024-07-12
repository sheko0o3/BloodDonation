from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password


from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


from database import models
from SerializerApp.serializers import UserInformationSerializer, UserSerializer
from FiltersApp.filters import SearchDonatorFilter




class ShowDonatorInfo(APIView):

    def get_object(self, pk):
        try:
            user = User.objects.get(id=pk)
            user_info = models.UserInformation.objects.get(user=user)
            return user_info

        except ObjectDoesNotExist:
            raise Http404


    def get(self,request):
        user = self.get_object(pk=request.data["user_id"])
        serializer = UserInformationSerializer(instance=user, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)



class SearchDonator(APIView):

    def get(self, request):
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

    def get(self, request):
        queryset = models.UserInformation.objects.all()
        serializer = UserInformationSerializer(instance=queryset, many=True) 
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    

class ResetData(APIView):
    pass


