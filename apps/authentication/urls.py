from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from apps.authentication import views

router = routers.DefaultRouter()
router.register('v1/auth', views.JWTAuthAPIView, basename='auth')

urlpatterns = [
    url('', include(router.urls)),
]
