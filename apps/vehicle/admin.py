from django.contrib import admin

# Register your models here.
from apps.vehicle import models

admin.site.register(models.Vehicle)
admin.site.register(models.TrackVehicle)
