from django.contrib.auth.models import User
from django.http import Http404
from django.core.exceptions import PermissionDenied
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from apps.people.models import Location, Notification
from apps.people.serializers import LocationSerializer, UserSerializer, NotificationSerializer, GCMTokenSerializer
from apps.people.tasks import run_alertdb_search, save_location_history
from statsd.defaults.django import statsd
from push_notifications.models import GCMDevice


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the location.
        return obj.owner == request.user


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    """
    def has_permission(self, request, view, obj=None):
        # Write permissions are only allowed to the owner of the location
        return obj is None or obj.user == request.user


class NotificationList(APIView):
    """
    List all notifications for authenticated user.
    """
    def get(self, request, format=None):

        notifs = Notification.objects.filter(user=request.user)
        serializer = NotificationSerializer(notifs, many=True)
        return Response(serializer.data)

    permission_classes = (IsAuthenticated,)


class NotificationDetail(APIView):
    """
    List notification details for authenticated user.
    """
    def get_object(self, pk):

        try:
            notif = Notification.objects.get(pk=pk)
            if notif.user == self.request.user:
                return notif
            else:
                raise PermissionDenied
        except Notification.DoesNotExist:
            raise Http404

    @statsd.timer('api.NotificationDertail.get')
    def get(self, request, pk, format=None):
        notif = self.get_object(pk)
        serializer = NotificationSerializer(notif)
        return Response(serializer.data)

    permission_classes = (IsAuthenticated,)


class UserList(APIView):
    """
    Creates new user proviles.
    """

    @statsd.timer('api.UserList.get')
    def post(self, request, format=None):

        data = request.DATA
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    permission_classes = (AllowAny,)


class GCMTokenList(APIView):
    """
    Creates and lists gcm proviles.
    """
    @statsd.timer('api.GCMTokenList.post')
    def post(self, request, format=None):

        data = request.DATA
        data['user'] = request.user.pk

        gcm_device = None
        if 'registration_id' in data:
            gcm_device = GCMDevice.objects.filter(registration_id=data['registration_id'], user=request.user)

        if gcm_device:
            serializer = GCMTokenSerializer(gcm_device[0], data=data)
        else:
            serializer = GCMTokenSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    permission_classes = (IsAuthenticated,)


class UserDetail(APIView):
    """
    Retrieve or update details of the authenticated user.
    """
    def get_object(self, pk):
        try:
            user = User.objects.get(pk=pk)
            if user == self.request.user:
                return user
            else:
                raise PermissionDenied
        except User.DoesNotExist:
            raise Http404

    @statsd.timer('api.UserDetail.get')
    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    permission_classes = (IsAuthenticated,)


class LocationList(APIView):
    """
    List all locations or create a new location for the authenticated user.
    """
    @statsd.timer('api.LocationList.get')
    def get(self, request, format=None):
        locations = Location.objects.filter(user=request.user)
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)

    @statsd.timer('api.LocationList.post')
    def post(self, request, format=None):
        statsd.incr('api.LocationList.post')
        data = request.DATA

        data['user'] = request.user.pk

        if data['source'] == "current":
            loc, created = Location.objects.get_or_create(source='current', user=request.user)
            serializer = LocationSerializer(loc, data=request.DATA)
        else:
            serializer = LocationSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    permission_classes = (IsAuthenticated,)


class LocationDetail(APIView):
    """
    Retrieve, update or delete location details for authenticated user.
    """
    def get_object(self, pk):
        try:
            loc = Location.objects.get(pk=pk)
            if loc.user == self.request.user:
                return loc
            else:
                raise PermissionDenied
        except Location.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        location = self.get_object(pk)
        serializer = LocationSerializer(location)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        location = self.get_object(pk)
        serializer = LocationSerializer(location, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        location = self.get_object(pk)
        serializer = LocationSerializer(location, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        location = self.get_object(pk)
        location.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


