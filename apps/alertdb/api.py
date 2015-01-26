from django.contrib.gis.geos import Point
from django.http import Http404, HttpResponse
from django.contrib.gis.measure import D
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, YAMLRenderer, XMLRenderer, BrowsableAPIRenderer
from rest_framework import status
from apps.alertdb.models import Alert, Info, Area
from apps.alertdb.serializers import AlertSerializer, AreaSerializer
from apps.alertdb.parsers import CAPXMLParser
from apps.alertdb.tasks import run_location_search
from statsd.defaults.django import statsd
import logging


class AlertListAPI(APIView):

    renderer_classes = (JSONRenderer, YAMLRenderer, BrowsableAPIRenderer, XMLRenderer)
    parser_classes = (CAPXMLParser,)

    @statsd.timer('api.AlertListAPI.get')
    def get(self, request):
        """
        Perform geospatial search for alerts. Also, respond to pubsubhubbub challenges.

        Geospatial searches require a lat and lng query parameter, both in WSG84 format. For instance:

        /api/v1/alerts/?lat=-33.5,lng=151

        """

        # This is to allow PubSubHubbub
        if 'hub.challenge' in request.QUERY_PARAMS:
            # This is just normal HttpResponse so it doesn't have quotes
            return HttpResponse(str(request.QUERY_PARAMS['hub.challenge']))

        try:
            lat = float(request.QUERY_PARAMS['lat'])
            lng = float(request.QUERY_PARAMS['lng'])
        except:
            raise Http404

        pnt = Point(lng, lat)
        info = Info.objects.filter(area__geom__distance_lt=(pnt, D(mi=3)))

        if len(info) > 0:
            info = info[0]
            alert = Alert.objects.get(info=info)
            serializer = AlertSerializer(alert)
            statsd.incr('api.AlertListAPI.get.success')
            return Response(serializer.data)
        else:
            statsd.incr('api.AlertListAPI.get.failure')
            raise Http404

    def post(self, request):
        """
        Create a new alert (POST). This endpoint accepts Common Alerting Protocal (CAP) 1.1 and 1.2, but does NOT accept
        ATOM/RSS feeds. In general, simply POST the entire XML message as the content of your request.

        """

        statsd.incr('api.AlertListAPI.post')
        timer = statsd.timer('api.AlertListAPI.post')
        timer.start()
        data = request.DATA
        try:
            for item in data:
                item['contributor'] = request.user.pk
        except Exception, e:
            logging.error(e)

        serializer = AlertSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            for s in serializer.data:
                if s['cap_status'] == 'Actual':  # This prevents any test messages from going out
                    run_location_search.delay(s['id'])
            statsd.incr('api.AlertListAPI.post.success')
            rsp = Response(status=status.HTTP_201_CREATED)
        else:
            statsd.incr('api.AlertListAPI.post.failure')
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
        serializer = AreaSerializer(areas)
        return Response(serializer.data)