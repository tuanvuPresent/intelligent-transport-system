from rest_framework import serializers

from apps.common.constant import ErrorCode
from apps.common.custom_exception_handler import CustomAPIException
from apps.vehicle.models import Vehicle, TrackVehicle, Owner

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ['id', 'name']

class VehicleSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    class Meta:
        model = Vehicle
        fields = ['id', 'vehicle_type', 'brand', 'name', 'color', 'license_plate', 'description', 'owner']

    def get_owner(self, instance):
        if instance.owner_id:
            return OwnerSerializer(instance.owner_id).data

class CreateOrUpdateVehicleSerializer(serializers.ModelSerializer):
    color = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    owner_name = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Vehicle
        fields = ['vehicle_type', 'brand', 'name', 'color', 'license_plate', 'description', 'owner_name']

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

    def create(self, validated_data):
        owner_name = validated_data.pop('owner_name')
        owner = Owner.objects.create(name=owner_name)
        vehicle = Vehicle.objects.create(owner_id=owner, **validated_data)
        return vehicle
    
    def update(self, instance, validated_data):
        owner_name = validated_data.pop('owner_name')
        instance = super().update(instance, validated_data)
        if instance.owner_id:
            instance.owner_id.name = owner_name or instance.owner_id.name
            instance.owner_id.save()
        else:
            owner = Owner.objects.create(name=owner_name)
            instance.owner_id = owner
            instance.save()
        return instance

class ListVehicleLocaltionSerializer(serializers.ModelSerializer):
    position = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    speed = serializers.SerializerMethodField()
    class Meta:
        model = Vehicle
        fields = ['id', 'vehicle_type', 'brand', 'name', 'color', 'license_plate', 'description', 'position', 'owner', 'speed']

    def get_position(self, instance):
        trackvehicle_list = instance.trackvehicle_set.all()
        result = []
        for item in trackvehicle_list:
            result.append({
                'lat':item.latitude,
                'lng': item.longitude,
                'speed': item.speed,
                'date': item.date,
            })
        return result
    
    def get_speed(self, instance):
        trackvehicle_list = instance.trackvehicle_set.all()
        if trackvehicle_list:
            return trackvehicle_list[0].speed
    
    def get_owner(self, instance):
        if instance.owner_id:
            return OwnerSerializer(instance.owner_id).data


class CreateVehicleLocaltionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackVehicle
        fields = ['date', 'longitude', 'latitude', 'speed', 'vehicle_id']


class CreateMultiVehicleLocaltionSerializer(serializers.Serializer):
    data = CreateVehicleLocaltionSerializer(many=True)

    def create(self, validated_data):
        list_location = validated_data.get('data')
        obj_list = []
        for item in list_location:
            obj_list.append(TrackVehicle(
                date=item.get('date'),
                longitude=item.get('longitude'),
                latitude=item.get('latitude'),
                speed=item.get('speed'),
                vehicle_id=item.get('vehicle_id')
            ))
        res = TrackVehicle.objects.bulk_create(obj_list)
        return res