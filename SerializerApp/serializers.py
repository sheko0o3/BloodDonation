from rest_framework import serializers

from django.contrib.auth.models import User


from database import models


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "username", "password", "Info")

        extra_kwargs = {
            "password": {
                "write_only": True,
                'style': {'input_type': 'password'}
                
            }
        }

        depth = 1




class UserInformationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UserInformation
        fields = ("id", "user", "bloodType", "name", "mobile", "govern",
                   "state", "Card_number",
                   "age","gender")
        
        

class UpdateInformationSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)



class ChangePasswordSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=True)
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)



class GovernSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Govern
        fields = "__all__"
        depth = 1


class StatesSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.GovernStates
        fields = "__all__"

class BloodTypesSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BloodType
        fields = ("id", "bloodtype", "user")
        depth = 1

