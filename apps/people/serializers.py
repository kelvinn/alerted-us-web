from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers
from apps.people.models import Location, Notification
from apps.alertdb.serializers import InfoSerializer
from push_notifications.models import GCMDevice

PASSWORD_MAX_LENGTH = User._meta.get_field('password').max_length


class UserSerializer(serializers.ModelSerializer):

    password_confirmation = serializers.CharField(max_length=PASSWORD_MAX_LENGTH)
    email = serializers.CharField(source='email', required='email' in User.REQUIRED_FIELDS)
    password = serializers.CharField(max_length=200, required=False, write_only=True)

    class Meta:
        model = User
        fields = (
            # required
            'username', 'email', 'password',
            # optional
            'first_name', 'last_name'
        )

    def restore_object(self, attrs, instance=None):
        # call set_password on user object. Without this
        # the password will be stored in plain text.
        user = super(UserSerializer, self).restore_object(attrs, instance)
        if 'password' in attrs:
            user.set_password(attrs['password'])
        return user


class GCMTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = GCMDevice
        fields = ('user', 'registration_id')


class LocationSerializer(gis_serializers.GeoModelSerializer):

    class Meta:
        model = Location
        fields = ('id', 'geom', 'name', 'user', 'source', 'date_received')


class NotificationSerializer(gis_serializers.GeoModelSerializer):
    user = UserSerializer()
    cap_info = InfoSerializer()

    class Meta:
        model = Notification
        fields = ('user', 'cap_info',)