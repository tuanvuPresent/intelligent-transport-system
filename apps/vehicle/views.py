# Create your views here.
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from django_filters import filters
from django_filters.rest_framework import FilterSet
from apps.common.custom_model_view_set import BaseModelViewSet
from apps.vehicle.models import Vehicle
from apps.vehicle.serializer import VehicleSerializer, CreateOrUpdateVehicleSerializer

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
        queryset = Vehicle.objects.all().order_by('id')
        return queryset
