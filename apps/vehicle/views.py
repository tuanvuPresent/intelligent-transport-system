# Create your views here.
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema

from apps.common.custom_model_view_set import BaseModelViewSet
from apps.vehicle.models import Vehicle
from apps.vehicle.serializer import VehicleSerializer, CreateOrUpdateVehicleSerializer


@method_decorator(name='partial_update', decorator=swagger_auto_schema(auto_schema=None))
class VehicleAPIView(BaseModelViewSet):
    serializer_action_classes = {
        'list': VehicleSerializer,
        'retrieve': VehicleSerializer,
        'create': CreateOrUpdateVehicleSerializer,
        'update': CreateOrUpdateVehicleSerializer,
    }

    allow_action_name = ['create', 'list', 'retrieve', 'update', 'destroy']

    def get_queryset(self):
        queryset = Vehicle.objects.all()
        return queryset
