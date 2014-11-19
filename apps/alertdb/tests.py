from django.utils import unittest
from django.contrib.auth.models import User
from django.test.client import Client
from django.contrib.gis.geos.collections import Point
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from apps.alertdb.models import Alert, Geocode
from apps.people.models import Location
from apps.alertdb.api import AlertListAPI, AlertDetailAPI
from apps.alertdb.tasks import run_location_search
from apps.alertdb.geocode_tools import GeocodeLoader

# Create API request factory
factory = APIRequestFactory()


class SimpleTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_front_page(self):

        response = self.client.get('/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):

        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)


class AlertdbAPITests(APITestCase):
    fixtures = ['alertdb_people_users']

    def setUp(self):
        self.cap_11_atom = open('apps/alertdb/testdata/amber.atom', 'r').read()
        self.cap_11 = open('apps/alertdb/testdata/weather.cap', 'r').read()
        self.cap_12 = open('apps/alertdb/testdata/australia.cap', 'r').read()
        self.cap_11b = open('apps/alertdb/testdata/weather_2.cap', 'r').read()
        self.signed_pelmorex = open('apps/alertdb/testdata/signed_pelmorex.cap', 'r').read()
        self.taiwan_cap_12 = open('apps/alertdb/testdata/taiwan.cap', 'r').read()
        self.ph_cap_12 = open('apps/alertdb/testdata/ph.cap', 'r').read()

    def test_subpub_hub_challenge_api(self):
        user, created = User.objects.get_or_create(username='apiuser')
        url = '/api/v1/alerts/?hub.challenge="kelvin"'

        view = AlertListAPI.as_view()
        request = factory.get(url)
        force_authenticate(request, user=user)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_alert(self):
        alert = Alert.objects.create(
            cap_slug="test", cap_sender="admin@alerted.us", cap_status="Actual",
            cap_message_type="Alert", cap_scope="Public"
        )
        alert2 = Alert.objects.get(cap_slug="test")
        self.assertEqual(alert, alert2)

    def test_alert_detail_get_api(self):
        user, created = User.objects.get_or_create(username='apiuser')
        alert = list(Alert.objects.all()[:1])[0]

        url = '/api/v1/alerts/%s/' % alert.cap_slug

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_alert_detail_get_404_api(self):
        url = '/api/v1/alerts/abcd/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_alert_api_post_cap11(self):
        user, created = User.objects.get_or_create(username='apiuser')
        url = '/api/v1/alerts/'

        view = AlertListAPI.as_view()
        request = factory.post(url, self.cap_11b, content_type='application/xml')
        force_authenticate(request, user=user)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # verify object created

        entry_result = list(Alert.objects.filter(cap_sender__contains='w-nws.webmaster@noaa.gov')[:1])[0]

        self.assertEqual(entry_result.cap_status, 'Actual')
        info_result = entry_result.info_set.get()

        self.assertEqual(info_result.cap_category, 'Met')

        area_result = list(info_result.area_set.all()[:1])[0]  # Get just one.

        self.assertIsNotNone(area_result.area_description)

    def test_alert_api_post_cap11_atom(self):
        user, created = User.objects.get_or_create(username='apiuser')
        url = '/api/v1/alerts/'

        view = AlertListAPI.as_view()
        request = factory.post(url, self.cap_11_atom, content_type='application/xml')
        force_authenticate(request, user=user)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # verify object created

        entry_result = list(Alert.objects.filter(cap_id__contains='http://doj.dc.gov/amber12345')[:1])[0]

        self.assertEqual(entry_result.cap_status, 'Actual')
        info_result = entry_result.info_set.get()

        self.assertEqual(info_result.cap_language, 'en-US')

        area_result = list(info_result.area_set.all()[:1])[0]  # Get just one.

        self.assertIsNotNone(area_result.area_description)

    def test_alert_api_put_cap12(self):
        user, created = User.objects.get_or_create(username='apiuser')
        url = '/api/v1/alerts/'

        view = AlertListAPI.as_view()
        request = factory.post(url, self.cap_12, content_type='application/xml')
        force_authenticate(request, user=user)

        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # verify object created

        entry_result = list(Alert.objects.filter(cap_id__contains='tag:www.rfs.nsw.gov.au2011-10-06:40184')[:1])[0]

        self.assertEqual(entry_result.cap_scope, 'Public')
        info_result = entry_result.info_set.all()[0]

        self.assertEqual(info_result.cap_urgency, 'Expected')

        area_result = list(info_result.area_set.all()[:1])[0]  # Get just one.

        self.assertIsNotNone(area_result.geom)

    def test_alert_api_put_taiwan_cap12(self):
        user, created = User.objects.get_or_create(username='apiuser')
        url = '/api/v1/alerts/'

        view = AlertListAPI.as_view()
        request = factory.post(url, self.taiwan_cap_12, content_type='application/xml')
        force_authenticate(request, user=user)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # verify object created

    def test_alert_api_put_ph_cap12(self):
        user, created = User.objects.get_or_create(username='apiuser')
        url = '/api/v1/alerts/'

        view = AlertListAPI.as_view()
        request = factory.post(url, self.ph_cap_12, content_type='application/xml')
        force_authenticate(request, user=user)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # verify object created

    def test_alert_api_query_by_coord(self):
        user, created = User.objects.get_or_create(username='apiuser')
        url = '/api/v1/alerts/?lng=-66.67249&lat=18.42207'

        view = AlertListAPI.as_view()
        request = factory.get(url)
        force_authenticate(request, user=user)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)  # verify we got back a response OK

        cap_sender = response.data['cap_sender']
        self.assertEqual(cap_sender, 'w-nws.webmaster@noaa.gov')  # test to sender

    def test_notification_via_alert(self):

        # First, create a test user and location
        p = Point(-67.188634, 18.381713)  # This point matches the alertdb fixture
        user, created = User.objects.get_or_create(username='test', email="dummy@kelvinism.com")
        loc = Location(user=user, geom=p)
        loc.save()

        # Next, get alerts and compare to locations
        alerts = Alert.objects.all()
        for alert in alerts:
            run_location_search.delay(alert.id)

        # Now run the tests
        self.assertEqual(loc.user.username, user.username)
        self.assertEqual(loc.geom, p)

    def test_alert_area_api(self):
        alert = list(Alert.objects.all()[:1])[0]
        url = "/api/v1/alerts/%s/areas/" % alert.cap_slug

        # Now test just listing locations
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # verify we got back a response OK

    def test_alert_area_get_404_api(self):
        url = '/api/v1/alerts/abcd/areas/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_alert_detail_view(self):
        alert = Alert.objects.all()[0]
        url = "/alerts/%s/" % alert.cap_slug
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # verify we got back a response OK

    def test_duplicate_alerts(self):
        # After an alert is created, I can't think of it as needing to be updated again
        user, created = User.objects.get_or_create(username='apiuser')
        url = '/api/v1/alerts/'

        view = AlertListAPI.as_view()
        request = factory.post(url, self.cap_11, content_type='application/xml')
        force_authenticate(request, user=user)
        response = view(request)

        request2 = factory.post(url, self.cap_11, content_type='application/xml')
        force_authenticate(request2, user=user)

        self.assertRaises(Exception, view, request2)


class AlertdbGeocodeTest(APITestCase):

    def setUp(self):
        self.g = GeocodeLoader()

    def test_run_philippines(self):
        self.g.run_philippines()
        result = Geocode.objects.get(code=36900000)
        self.assertEqual(result.name, "Tarlac")