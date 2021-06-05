import logging
from pyicloud import PyiCloudService
from django.conf import settings
from apps.vehicle.models import TrackVehicle, Vehicle
from datetime import datetime, timedelta
from geopy.distance import geodesic
from django.db.models import Prefetch

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
        vehicle = Vehicle.objects.all().prefetch_related(
            Prefetch(
                'trackvehicle_set',
                queryset=TrackVehicle.objects.all().order_by('-date'),
            )
        ).first()
        if vehicle:
            trackvehicle = vehicle.trackvehicle_set.all()
            speed = 0
            if len(trackvehicle) > 0:
                localtion_last = trackvehicle[0].latitude, trackvehicle[0].longitude
                t1 = trackvehicle[0].date.timestamp()
                t2 = datetime.now().astimezone().timestamp()
                if t2 - t1 < 20:
                    speed = 3.6 * geodesic(localtion_last, (lat, lng)).meters / (t2 - t1)
            TrackVehicle.objects.create(
                date=now,
                longitude=lng,
                latitude=lat,
                vehicle_id=vehicle,
                speed=speed
            )
    except:
        pass
