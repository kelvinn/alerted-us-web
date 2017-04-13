from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometrySerializerMethodField
from rest_framework import serializers
from apps.alertdb.models import Alert, Info, Area, Parameter, Resource
from statsd.defaults.django import statsd


class ResourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Resource
        fields = '__all__'


class ParameterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Parameter
        fields = '__all__'


class AreaSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = Area
        geo_field = 'geom'
        fields = ('area_description', 'geocode_list', 'geom')

    def create(self, validated_data):
        info_data_set = validated_data.pop('info_set')
        cap_alert = Alert.objects.create(**validated_data)
        for info_data in info_data_set:
            area_data_set = info_data.pop('area_set')
            cap_info = Info.objects.create(cap_alert=cap_alert, **info_data)
            for area_data in area_data_set:
                Area.objects.create(cap_info=cap_info, **area_data)
        return cap_alert


class InfoSerializer(serializers.ModelSerializer):
    parameter_set = ParameterSerializer(many=True, required=False)
    resource_set = ResourceSerializer(many=True, required=False)
    area_set = AreaSerializer(many=True, required=False)

    class Meta:
        model = Info
        fields = '__all__'


class AlertSerializer(serializers.ModelSerializer):
    info_set = InfoSerializer(many=True)

    class Meta:
        model = Alert
        fields = '__all__'
        depth = 1

    def create(self, validated_data):
        info_data_set = validated_data.pop('info_set')
        cap_alert = Alert.objects.create(**validated_data)
        for info_data in info_data_set:
            area_data_set = info_data.pop('area_set')
            cap_info = Info.objects.create(cap_alert=cap_alert, **info_data)
            for area_data in area_data_set:
                Area.objects.create(cap_info=cap_info, **area_data)
        return cap_alert

