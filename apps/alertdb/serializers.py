from os import getenv
from rest_framework_gis import serializers as gis_serializers
from rest_framework import serializers
from apps.alertdb.models import Alert, Info, Area, Parameter, Resource
from statsd.defaults.django import statsd
import redis

redis_url = getenv('REDISCLOUD_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)

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
