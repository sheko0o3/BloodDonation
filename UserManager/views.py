from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password


from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


from database import models
from SerializerApp.serializers import UserInformationSerializer, UserSerializer




class SaveUserInformation(APIView):

    def post(self, request):
        serializer = UserInformationSerializer(data=request.data)
        if serializer.is_valid():
            user_info= models.UserInformation.objects.create(
                user = User.objects.get(id=request.data["user"]),
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
    def get_user(self,request):
        try:
            user = User.objects.get(id=request.data["user"])
            user_info = models.UserInformation.objects.get(user=user)
            return user_info

        except ObjectDoesNotExist:

            raise Http404
            

    def get(self, request):
        try:
            user = User.objects.get(id=request.data["user"])
            user_info = models.UserInformation.objects.get(user=user)
            serializer = UserInformationSerializer(instance=user_info, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:

            return Response(data={"message": "NOT FOUND!"}, status=status.HTTP_404_NOT_FOUND)


    def put(self, request):
        # try:
        #     user = User.objects.get(id=request.data["user"])
        #     user_info = models.UserInformation.objects.get(user=user)
        # except ObjectDoesNotExist:
        #     return Response(data={"message": "NOT FOUND!"}, status=status.HTTP_404_NOT_FOUND)
        user_info = self.get_user(request=request)

        if user_info.user.check_password(request.data["password"]):
            serializer = UserInformationSerializer(instance=user_info, data=request.data)
            if serializer.is_valid():
                serializer.save(password=make_password(request.data["password"]))
                serializer.help_text = "Update Success"
                return Response(data={"message": serializer.help_text}, status=status.HTTP_202_ACCEPTED)
            return Response(data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(data={"message": "Wrong Password!"}, status=status.HTTP_401_UNAUTHORIZED)
    


        
class DeleteUser(APIView):
    def get_user(self,request):
        try:
            user = User.objects.get(id=request.data["user"])
            return user
        except ObjectDoesNotExist:

            raise Http404
            

    def delete(self, request):
        # try:
        #     user = User.objects.get(id=request.data["user"])
        
        # except ObjectDoesNotExist:

        #     return Response(data={"message": "NOT FOUND!"}, status=status.HTTP_404_NOT_FOUND) 
        user = self.get_user(request=request)
        if user.check_password(request.data["password"]):
            user.delete()
            return Response(data={"messgae": "Account Deleted"}, status=status.HTTP_204_NO_CONTENT)
        return Response(data={"message":"Wrong Password!"}, status=status.HTTP_204_NO_CONTENT)
