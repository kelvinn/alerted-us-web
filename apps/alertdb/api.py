from django.contrib.gis.geos import Point
from django.http import Http404, HttpResponse
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
        info = Info.objects.filter(area__geom__intersects=pnt)

        if len(info) > 0:
            info = info[0]
            alert = Alert.objects.get(info=info)
            serializer = AlertSerializer(alert)
            return Response(serializer.data)
        else:
            raise Http404

    # @statsd.timer('api.AlertListAPI.post')
    def post(self, request, format=None):
        """
        Create a new alert (POST). This endpoint accepts Common Alerting Protocal (CAP) 1.1 and 1.2, but does NOT accept
        ATOM/RSS feeds. In general, simply POST the entire XML message as the content of your request.

        """

        statsd.incr('api.AlertListAPI.post')
        timer = statsd.timer('api.AlertListAPI.post')
        timer.start()
        data = request.DATA
        timer4 = statsd.timer('api.AlertListAPI.contributor')
        timer4.start()
        try:
            data[0]['contributor'] = request.user.pk
        except:
            logging.error("Invalid XML so unable to add contributor")
        timer4.stop()
        timer2 = statsd.timer('api.AlertListAPI.post.serializer')
        timer2.start()
        serializer = AlertSerializer(data=data)
        timer2.stop()
        timer5 = statsd.timer('api.AlertListAPI.post.is_valid_outside')
        timer5.start()
        if serializer.is_valid():
            timer3 = statsd.timer('api.AlertListAPI.post.is_valid')
            timer3.start()
            serializer.save()
            for s in serializer.data:
                if s['cap_status'] == 'Actual':  # This prevents any test messages from going out
                    run_location_search.delay(s['id'])
            rsp = Response(status=status.HTTP_201_CREATED)
            timer3.stop()
        else:
            statsd.incr('api.AlertListAPI.post.not_valid')
            logging.info("Invalid XML detected")
            timer6 = statsd.timer('api.AlertListAPI.post.respones')
            timer6.start()
            rsp = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            timer6.stop()
        timer.stop()
        timer5.stop()
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
    def get(self, request, cap_slug, format=None):
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
    def get(self, request, cap_slug, format=None):

        alert = self.get_object(cap_slug)
        areas = Area.objects.filter(cap_info__cap_alert=alert)
        serializer = AreaSerializer(areas)
        return Response(serializer.data)