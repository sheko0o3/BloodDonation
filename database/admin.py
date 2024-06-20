from django.contrib import admin

from . import models


admin.site.register(models.BloodType)
admin.site.register(models.UserInformation)
admin.site.register(models.Govern)
admin.site.register(models.GovernState)
admin.site.register(models.Donation)

