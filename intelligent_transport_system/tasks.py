import logging
from pyicloud import PyiCloudService
from django.conf import settings
from apps.vehicle.models import TrackVehicle, Vehicle
from datetime import datetime

def tracking_vehicle():
    logger = logging.getLogger()
    logger.error('start')
    try:
        username = settings.ICLOUD_USERNAME
        password = settings.ICLOUD_PASSWORD
        api = PyiCloudService(username, password)
        location = api.iphone.location()
        lat, lng = location.get('latitude'), location.get('longitude')
        now = datetime.now()
        vehicle_id = Vehicle.objects.all().first()
        if vehicle_id:
            TrackVehicle.objects.create(
                date=now,
                longitude=lng,
                latitude=lat,
                vehicle_id=vehicle_id,
                speed=0
            )
    except:
        pass
