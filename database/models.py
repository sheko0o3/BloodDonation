from django.db import models


from django.contrib.auth.models import User


class Gender(models.TextChoices):
    Male = "Male"
    Female = "Female"


class BloodType(models.Model):
    bloodtype = models.CharField(max_length=10, unique=True)

    def __str__(self) -> str:
        return self.bloodType
    

class Govern(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name
    


class GovernState(models.Model):
    govername = models.ForeignKey(to=Govern, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, unique=True)

    def __str__(self) -> str:
        return self.name
    

class Donation(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date_of_donation = models.DateField()



class UserInformation(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name="Info")
    bloodType = models.ForeignKey(to=BloodType,null=True, on_delete=models.SET_NULL, related_name="users" )
    name = models.CharField(max_length=50, null=False, blank=False)
    mobile = models.CharField(max_length=11, null=False, blank=False, unique=True)
    govern = models.ForeignKey(to=Govern, null=True, on_delete=models.SET_NULL)
    state = models.ForeignKey(to=GovernState, null=True, on_delete=models.SET_NULL)
    Card_number = models.CharField(max_length=14, null=False, blank=False, unique=True)
    date_of_donation = models.DateTimeField(null=True, blank=True)
    age = models.IntegerField(null=False, blank=False)
    gender = models.CharField(max_length=20, choices=Gender.choices, null=False, blank=False)
    
    

    def __str__(self) -> str:
        return self.user.username


