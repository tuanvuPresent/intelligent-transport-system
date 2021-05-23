from geopy.distance import geodesic, great_circle
from datetime import datetime, timedelta
import random
import math
from .models import TrackVehicle, Vehicle

direct_list = [
    (1, -1), (1, 0), (1, 1), (0, 1),  
    (-1, 1), (-1, 0), (-1, -1), (0, -1),
]

rate_direction = [
    [0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,2,2,3,5,6,6,7,7,7],
    [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,3,3,4,6,7,7],
    [0,0,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,4,4,5,7],
    [1,1,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,5,5,6,0],
    [4,4,4,4,4,4,4,4,4,4,4,4,5,5,5,6,6,7,3,3,3,2,2,1],
    [5,5,5,5,5,5,5,5,5,5,5,5,6,6,6,7,7,0,4,4,4,3,3,2],
    [6,6,6,6,6,6,6,6,6,6,6,6,7,7,7,0,0,5,5,5,4,4,3,1],
    [7,7,7,7,7,7,7,7,7,7,7,7,0,0,0,6,6,6,1,1,5,5,4,2],
]

def get_location_next(localtion_current, direct):
    speed = random.randint(55, 155) / 10
    distance = 20 * speed / math.sqrt(direct[0] * direct[0] + direct[1] * direct[1])
    lat = localtion_current[0] + (direct[0] * distance) / 111320
    lng = localtion_current[1] + (direct[1] * distance) / (math.cos(localtion_current[0]) * 111320)
    return lat, lng

def get_direct_next(direct_current):
    rate = None
    for index, item in enumerate(direct_list):
        if item == direct_current:
            rate = rate_direction[index]
            break
    index = rate[random.randint(0, len(rate) - 1)]
    direct_next = direct_list[index]
    return direct_next

def seed_data_localtion(minutes):
    data = []
    vehicle = Vehicle.objects.first()
    vehicle_id = None
    if vehicle:
        vehicle_id = vehicle.id
    vehicle_list = Vehicle.objects.all().exclude(id=vehicle_id)
    TrackVehicle.objects.filter(date__gte=datetime.now()).delete()
    for item in vehicle_list:
        direct_current = direct_list[random.randint(0, 7)]
        localtion_current = random.randint(2100, 2200) / 100, random.randint(1050, 1060) / 10
        current_time = datetime.now()
        for i in range(minutes * 3):
            direct_next = get_direct_next(direct_current)
            localtion_next = get_location_next(localtion_current, direct_current)
            speed = 3.6 * geodesic(localtion_next, localtion_current).meters / 20
            current_time += timedelta(seconds=20)
            
            data.append(
                TrackVehicle(
                    date=current_time,
                    latitude=localtion_next[0],
                    longitude=localtion_next[1],
                    speed=speed,
                    vehicle_id=item
                )    
            )
            direct_current = direct_next
            localtion_current = localtion_next
    return data
