# Create your views here.
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from django_filters import filters
from django_filters.rest_framework import FilterSet
from apps.common.custom_model_view_set import BaseModelViewSet
from apps.vehicle.models import Vehicle, TrackVehicle
from apps.vehicle.serializer import VehicleSerializer, CreateOrUpdateVehicleSerializer, ListVehicleLocaltionSerializer, CreateMultiVehicleLocaltionSerializer
from datetime import datetime
from django.db.models import Prefetch
from rest_framework.response import Response
from intelligent_transport_system.tasks import tracking_vehicle

class VehicleFilter(FilterSet):
    vehicle_type = filters.CharFilter(field_name='vehicle_type', lookup_expr='exact')
    brand = filters.CharFilter(field_name='brand', lookup_expr='icontains')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    license_plate = filters.CharFilter(field_name='license_plate', lookup_expr='icontains')

@method_decorator(name='partial_update', decorator=swagger_auto_schema(auto_schema=None))
class VehicleAPIView(BaseModelViewSet):
    filter_class = VehicleFilter
    authentication_classes = []
    serializer_action_classes = {
        'list': VehicleSerializer,
        'retrieve': VehicleSerializer,
        'create': CreateOrUpdateVehicleSerializer,
        'update': CreateOrUpdateVehicleSerializer,
    }

    allow_action_name = ['create', 'list', 'retrieve', 'update', 'destroy']

    def get_queryset(self):
        queryset = Vehicle.objects.all().select_related('owner_id').order_by('id')
        return queryset


@method_decorator(name='retrieve', decorator=swagger_auto_schema(auto_schema=None))
@method_decorator(name='update', decorator=swagger_auto_schema(auto_schema=None))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(auto_schema=None))
@method_decorator(name='destroy', decorator=swagger_auto_schema(auto_schema=None))
class VehicleLocaltionAPIView(BaseModelViewSet):
    authentication_classes = []
    serializer_action_classes = {
        'list': ListVehicleLocaltionSerializer,
        'create': CreateMultiVehicleLocaltionSerializer,
    }

    allow_action_name = ['create', 'list']

    def get_queryset(self):
        queryset = Vehicle.objects.all().select_related('owner_id').prefetch_related(
            Prefetch(
                'trackvehicle_set',
                queryset=TrackVehicle.objects.filter(date__lte=datetime.now()).order_by('-date'),
            )
        )
        return queryset 
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(None)

    def list(self, request, *args, **kwargs):
        tracking_vehicle()
        return super().list(request, *args, **kwargs)