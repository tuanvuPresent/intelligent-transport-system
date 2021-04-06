from django.db import models

from apps.common.models import BaseModel
from apps.vehicle.constants import VehicleType


class Vehicle(BaseModel):
    vehicle_type = models.IntegerField(choices=[(item.value, item.value) for item in VehicleType],
                                       default=VehicleType.CAR.value)
    brand = models.CharField(max_length=32)
    name = models.CharField(max_length=128)
    color = models.CharField(max_length=32)
    license_plate = models.CharField(max_length=64)
    description = models.CharField(max_length=512)


class TrackVehicle(BaseModel):
    date = models.DateTimeField()
    longitude = models.CharField(max_length=32)
    latitude = models.CharField(max_length=32)
    speed = models.CharField(max_length=32)

    vehicle_id = models.ForeignKey('Vehicle', models.CASCADE)
