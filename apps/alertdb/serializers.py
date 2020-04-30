from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometrySerializerMethodField
from rest_framework import serializers
from apps.alertdb.models import Alert, Info, Area, Parameter, Resource
from statsd.defaults.django import statsd


class ResourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Resource
        exclude = ['cap_info']


class ParameterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Parameter
        exclude = ['cap_info']

    def create(self, validated_data):
        info_data_set = validated_data.pop('info_set')
        cap_alert = Alert.objects.get_or_create(**validated_data)
        for info_data in info_data_set:
            parameter_data_set = info_data.pop('parameter_set')
            cap_info = Info.objects.get_or_create(cap_alert=cap_alert, **info_data)
            for parameter_data in parameter_data_set:
                Parameter.objects.create(cap_info=cap_info, **parameter_data)
        return cap_alert


class AreaSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = Area
        geo_field = 'geom'
        fields = ['area_description', 'geocode_list', 'geom']


class InfoSerializer(serializers.ModelSerializer):
    area_set = AreaSerializer(many=True, required=False)
    resource_set = ResourceSerializer(many=True, required=False)
    parameter_set = ParameterSerializer(many=True, required=False)

    class Meta:
        model = Info
        fields = '__all__'

    def create(self, validated_data):
        area_set = validated_data.pop('area_set', [])
        resource_set = validated_data.pop('resource_set', [])
        parameter_set = validated_data.pop('parameter_set', [])

        cap_info = Info.objects.create(**validated_data)

        for area_data in area_set:
            Area.objects.create(cap_info=cap_info, **area_data)

        for resource_data in resource_set:
            Resource.objects.create(cap_info=cap_info, **resource_data)

        for parameter_data in parameter_set:
            Parameter.objects.create(cap_info=cap_info, **parameter_data)

        return cap_info


class AlertSerializer(serializers.ModelSerializer):
    info_set = InfoSerializer(many=True, required=False)

    class Meta:
        model = Alert
        fields = '__all__'

    def create(self, validated_data):
        info_validated_data = validated_data.pop('info_set')
        alert_obj = Alert.objects.create(**validated_data)
        info_set_serializer = self.fields['info_set']
        for each in info_validated_data:
            each['cap_alert'] = alert_obj
        info_set_serializer.create(info_validated_data)
        return alert_obj
