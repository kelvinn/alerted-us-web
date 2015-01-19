from django.utils import unittest
from django.contrib.gis.geos.collections import Point
from django.contrib.auth.models import User
from django.test.client import Client

from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework import status
from push_notifications.models import GCMDevice
from apps.people.models import Location, Notification
from apps.people.tasks import *
import re
import time


# Create your tests here.
factory = APIRequestFactory()


class SimpleTest(unittest.TestCase):

    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_add_location(self):
        p = Point(-67.188634, 18.381713)

        user, created = User.objects.get_or_create(username='testuser')

        loc = Location(user=user, geom=p)
        loc.save()
        self.assertEqual(loc.user.username, user.username)
        self.assertEqual(loc.geom, p)


class SimpleTest(unittest.TestCase):
    def test_save_location_history(self):
        user, created = User.objects.get_or_create(username='apiuser')
        loc = Location.objects.create(user=user, name="Test", source="static")
        result = save_location_history(loc)
        self.assertTrue(result)

    def test_run_alertdb_search(self):
        user, created = User.objects.get_or_create(username='apiuser')
        loc = Location.objects.create(user=user, name="Test", source="static")
        result = run_alertdb_search(loc)
        self.assertTrue(result)


class PeopleTests(APITestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_past_alerts_view(self):
        User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        url = '/dashboard/past-alerts/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_settings_view(self):
        User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        url = '/dashboard/settings/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_locations_view(self):
        User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        url = '/dashboard/locations/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LocationAPITests(APITestCase):
    def test_add_location_api(self):

        user, created = User.objects.get_or_create(username='apiuser')

        url = '/api/v1/users/locations/'
        data = {u'geom': {u'type': u'Point', u'coordinates': [-67.188634, 18.381713]},
                u'name': u'Aguada, 00602, Puerto Rico',
                u'source': u'static'}

        self.client.force_authenticate(user=user)

        # Test creating a list
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Now test just listing locations
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_location_detail_api(self):
        user, created = User.objects.get_or_create(username='apiuser')
        url = '/api/v1/users/locations/'
        data = {u'geom': {u'type': u'Point', u'coordinates': [-67.188634, 18.381713]},
                u'name': u'Aguada, 00602, Puerto Rico',
                u'source': u'static'}

        self.client.force_authenticate(user=user)

        # Test creating a list (POST)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test creating an invalid list (POST)
        data = {u'geom': u'invalid',
                u'name': u'Aguada, 00602, Puerto Rico',
                u'source': u'static'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test GET
        loc = Location.objects.get()
        url = '/api/v1/users/locations/%s/' % loc.pk
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {u'name': u'Success', u'user': user.pk}

        # Now test PATCH
        url = '/api/v1/users/locations/%s/' % loc.pk
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Now test PUT
        url = '/api/v1/users/locations/%s/' % loc.pk
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Now test DELETE
        url = '/api/v1/users/locations/%s/' % loc.pk
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Try to access an invalid location
        url = '/api/v1/users/locations/99/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class NotificationAPITests(APITestCase):
    # python manage.py dumpdata auth.user alertdb people > alertdb_people_users.json
    fixtures = ['alertdb_people_users']

    def test_get_notification_api(self):

        user, created = User.objects.get_or_create(username='apiuser')

        url = '/api/v1/users/notifications/'

        self.client.force_authenticate(user=user)

        # Test creating a list
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_notification_detail_api(self):

        notif = Notification.objects.get()
        user = notif.user
        url = '/api/v1/users/notifications/%s/' % notif.pk

        self.client.force_authenticate(user=user)

        # Test creating a list
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = '/api/v1/users/notifications/99/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UserAPITests(APITestCase):

    def test_create_user_api(self):
        url = '/api/v1/users/'

        data = {u'username': u'admin@alerted.us', u'email': u'admin@alerted.us', u'password': u'password'}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_patch_user_api(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        url = '/api/v1/users/%s/' % user.pk
        data = {u'username': user.username, u'email': u'test@alerted.us'}

        self.client.force_authenticate(user=user)
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = '/api/v1/users/10/'

        self.client.force_authenticate(user=user)
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_users_api(self):

        user, created = User.objects.get_or_create(username='testuser')
        url = '/api/v1/users/profiles/%s/' % user.pk

        self.client.force_authenticate(user=user)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_gcm_token(self):

        user, created = User.objects.get_or_create(username='apiuser')

        data = {u'registration_id': u'1234'}

        self.client.force_authenticate(user=user)

        # Test creating a gcm token
        url = '/api/v1/users/gcmtoken/'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test re-updating the gcm token
        url = '/api/v1/users/gcmtoken/'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test that it was only created once
        gcm_count = len(GCMDevice.objects.filter(user=user))
        self.assertEqual(gcm_count, 1)

        # Test creating an invalid gcm token
        data = {u'registration_123': u'1234'}
        url = '/api/v1/users/gcmtoken/'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_token(self):
        #user, created = User.objects.get_or_create(username='admin', password='password')

        user = User.objects.create_user(username='admin', password='password')


        data = {u'username': u'admin', u'password':u'password'}

        # Test getting auth token
        url = '/api-token-auth/'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
