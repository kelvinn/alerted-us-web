from os import getenv
from rest_framework_gis import serializers as gis_serializers
from rest_framework import serializers
from apps.alertdb.models import Alert, Info, Area, Parameter, Resource
from statsd.defaults.django import statsd


class ResourceSerializer(gis_serializers.GeoModelSerializer):

    class Meta:
        model = Resource


class ParameterSerializer(gis_serializers.GeoModelSerializer):

    class Meta:
        model = Parameter


class AreaSerializer(gis_serializers.GeoFeatureModelSerializer):

    class Meta:
        model = Area
        geo_field = "geom"

    def create(self, validated_data):
        info_data_set = validated_data.pop('info_set')
        cap_alert = Alert.objects.create(**validated_data)
        for info_data in info_data_set:
            area_data_set = info_data.pop('area_set')
            cap_info = Info.objects.create(cap_alert=cap_alert, **info_data)
            for area_data in area_data_set:
                Area.objects.create(cap_info=cap_info, **area_data)
        return cap_alert


class InfoSerializer(gis_serializers.GeoModelSerializer):
    parameter_set = ParameterSerializer(many=True, required=False)
    resource_set = ResourceSerializer(many=True, required=False)
    area_set = AreaSerializer(many=True, required=False)

    class Meta:
        model = Info



class AlertSerializer(gis_serializers.GeoModelSerializer):
    info_set = InfoSerializer(many=True)

    class Meta:
        model = Alert
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

