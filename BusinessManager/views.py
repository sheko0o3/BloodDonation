from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


from SerializerApp.serializers import (GovernSerializer,StatesSerializer,BloodTypesSerializer)
from database import models



class AllGoverns(APIView):

    def get(self, request):
        queryset = models.Govern.objects.all().order_by("name")
        serializer = GovernSerializer(instance=queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    


class AllStates(APIView):

    def get(self, request):
        queryset = models.GovernStates.objects.all().order_by("name")
        serializer = StatesSerializer(instance=queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    


class AllBloodTypes(APIView):

    def get(self, request):
        queryset = models.BloodType.objects.all()
        serializer = BloodTypesSerializer(instance=queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)