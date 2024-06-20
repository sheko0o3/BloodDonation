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


class BloodTypesSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BloodType
        fields = ("id", "bloodtype", "users")
        depth = 1



class UserInformationSerializer(serializers.ModelSerializer):
    bloodType = serializers.SlugRelatedField(queryset=models.BloodType.objects.all(), slug_field="bloodtype")
    govern = serializers.SlugRelatedField(queryset=models.Govern.objects.all(), slug_field="name")
    state = serializers.SlugRelatedField(queryset=models.GovernState.objects.all(), slug_field="name")
        
    class Meta:
        model = models.UserInformation
        fields = ("id", "user", "bloodType", "name", "mobile", "govern",
                   "state", "Card_number",
                   "age","gender","date_of_donation")
    



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
        model = models.GovernState
        fields = "__all__"

