from django.db import models

from apps.common.models import BaseModel
from apps.vehicle.constants import VehicleType


class Owner(BaseModel):
    name = models.CharField(max_length=32)


class Vehicle(BaseModel):
    vehicle_type = models.IntegerField(choices=[(item.value, item.value) for item in VehicleType],
                                       default=VehicleType.CAR.value)
    brand = models.CharField(max_length=32)
    name = models.CharField(max_length=128)
    color = models.CharField(max_length=32)
    license_plate = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    owner_id = models.ForeignKey('Owner', models.CASCADE, null=True)


class TrackVehicle(BaseModel):
    date = models.DateTimeField()
    longitude = models.FloatField()
    latitude = models.FloatField()
    speed = models.FloatField()

    vehicle_id = models.ForeignKey('Vehicle', models.CASCADE)
