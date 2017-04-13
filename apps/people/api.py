from django.contrib.auth.models import User
from django.http import Http404
from django.core.exceptions import PermissionDenied
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from apps.people.models import Location
from apps.people.serializers import LocationSerializer, UserSerializer
from statsd.defaults.django import statsd


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


class UserList(APIView):
    """
    Creates new user proviles.
    """

    @statsd.timer('api.UserList.post')
    def post(self, request, format=None):

        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    permission_classes = (AllowAny,)


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
        serializer = UserSerializer(user, data=request.data, partial=True)

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
        data = request.data

        data['user'] = request.user.pk

        if data['source'] == "current":
            loc, created = Location.objects.get_or_create(source='current', user=request.user)
            serializer = LocationSerializer(loc, data=request.data)
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
        serializer = LocationSerializer(location, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        location = self.get_object(pk)
        serializer = LocationSerializer(location, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        location = self.get_object(pk)
        location.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


