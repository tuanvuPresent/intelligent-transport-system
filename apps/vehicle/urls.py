from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from apps.vehicle import views

router = routers.DefaultRouter()
router.register('v1/vehicles', views.VehicleAPIView, basename='vehicle')

urlpatterns = [
    url('', include(router.urls)),
]
