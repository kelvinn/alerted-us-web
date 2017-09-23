from django.contrib.gis.geos import Point
from django.http import Http404, HttpResponse
from django.contrib.gis.measure import D
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework import status
from apps.alertdb.models import Alert, Info, Area
from apps.alertdb.serializers import AlertSerializer, AreaSerializer
from apps.alertdb.parsers import CAPXMLParser
from statsd.defaults.django import statsd
from datetime import datetime
import logging


class AlertListAPI(APIView):
    """
    get:
    Return a list of all the existing alerts.

    post:
    Create a new CAP-based alert.
    """
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)
    parser_classes = (CAPXMLParser,)

    @statsd.timer('api.AlertListAPI.get')
    def get(self, request):
        """
        Perform geospatial search for alerts. Also, respond to pubsubhubbub challenges.

        Geospatial searches require a lat and lng query parameter, both in WSG84 format. For instance:

        /api/v1/alerts/?lat=-33.5,lng=151

        """

        # This is to allow PubSubHubbub
        if 'hub.challenge' in request.query_params:
            # This is just normal HttpResponse so it doesn't have quotes
            return HttpResponse(str(request.query_params['hub.challenge']))

        try:
            lat = float(request.query_params['lat'])
            lng = float(request.query_params['lng'])
        except:
            raise Http404

        if 'cap_date_received' in request.query_params:
            cap_date_received = str(request.query_params['cap_date_received'])
        else:
            cap_date_received = None

        pnt = Point(lng, lat)

        if cap_date_received is not None:
            alert = Alert.objects.filter(
                cap_date_received__gte=cap_date_received
            )
        else:
            alert = Alert.objects.all()

        alert = alert.filter(
            #info__area__geom__dwithin=(pnt, 0.02)
            info__area__geom__dwithin=(pnt, D(m=2000))
        ).filter(
            info__cap_expires__gte=datetime.now()
        ).prefetch_related('info_set')

        """
        alert = alert.filter(
            info__area__geom__dwithin=(pnt, 0.02)
        ).filter(
            info__cap_expires__gte=datetime.now()
        )
        """

        if len(alert) > 0:
            serializer = AlertSerializer(alert, many=True)
            return Response(serializer.data)
        else:
            raise Http404

    def post(self, request):
        """
        Create a new alert (POST). This endpoint accepts Common Alerting Protocal (CAP) 1.1 and 1.2, but does NOT accept
        ATOM/RSS feeds. In general, simply POST the entire XML message as the content of your request.

        """

        statsd.incr('api.AlertListAPI.post')
        timer = statsd.timer('api.AlertListAPI.post')
        timer.start()
        data = request.data
        try:
            for item in data:
                item['contributor'] = request.user.pk
        except Exception, e:
            logging.error(e)

        serializer = AlertSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            rsp = Response(status=status.HTTP_201_CREATED)
        else:
            rsp = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        timer.stop()
        return rsp


class AlertDetailAPI(APIView):
    """
    Retrieve details about an alert.
    """

    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)

    def get_object(self, cap_slug):
        try:
            alert = Alert.objects.get(cap_slug=cap_slug)
            return alert
        except Alert.DoesNotExist:
            raise Http404

    @statsd.timer('api.AlertDetailAPI.get')
    def get(self, request, cap_slug):
        alert = self.get_object(cap_slug)
        serializer = AlertSerializer(alert)
        return Response(serializer.data)


class AlertAreaAPI(APIView):
    """
    Retrive area details for a given alert.
    """

    def get_object(self, cap_slug):
        try:
            alert = Alert.objects.get(cap_slug=cap_slug)
            return alert
        except Alert.DoesNotExist:
            raise Http404

    @statsd.timer('api.AlertAreaAPI.get')
    def get(self, request, cap_slug):

        alert = self.get_object(cap_slug)
        areas = Area.objects.filter(cap_info__cap_alert=alert)
        serializer = AreaSerializer(areas, many=True)
        return Response(serializer.data)