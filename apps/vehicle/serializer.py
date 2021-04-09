from rest_framework import serializers

from apps.common.constant import ErrorCode
from apps.common.custom_exception_handler import CustomAPIException
from apps.vehicle.models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'vehicle_type', 'brand', 'name', 'color', 'license_plate', 'description']


class CreateOrUpdateVehicleSerializer(serializers.ModelSerializer):
    color = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    class Meta:
        model = Vehicle
        fields = ['vehicle_type', 'brand', 'name', 'color', 'license_plate', 'description']

    def validate(self, attrs):
        license_plate = attrs.get('license_plate')
        request = self.context.get('request')
        if request.method == 'POST':
            if license_plate and Vehicle.objects.filter(license_plate=license_plate).first():
                raise CustomAPIException(ErrorCode.LICENSE_PLATE)
        else:
            if self.instance.license_plate != license_plate \
                    and Vehicle.objects.filter(license_plate=license_plate).first():
                raise CustomAPIException(ErrorCode.LICENSE_PLATE)

        return attrs
