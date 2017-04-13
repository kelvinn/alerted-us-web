from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers
from apps.people.models import Location
from apps.alertdb.serializers import InfoSerializer

PASSWORD_MAX_LENGTH = User._meta.get_field('password').max_length


class UserSerializer(serializers.ModelSerializer):

    email = serializers.CharField(required='email' in User.REQUIRED_FIELDS)
    password = serializers.CharField(max_length=200, required=False, write_only=True)

    class Meta:
        model = User
        fields = (
            # required
            'username', 'email', 'password',
            # optional
            'first_name', 'last_name'
        )

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
        return user



    """
    def create(self, validated_data):
        # call set_password on user object. Without this
        # the password will be stored in plain text.
        user = super(UserSerializer, self).restore_object(validated_data)
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
        return user
        
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user
        
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
        return user
    """


class LocationSerializer(gis_serializers.GeoModelSerializer):

    class Meta:
        model = Location
        fields = ('id', 'geom', 'name', 'user', 'source', 'date_received')