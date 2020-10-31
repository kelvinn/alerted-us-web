# pylint: disable=E1120
from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.gis.geos import GeometryCollection
from apps.alertdb.models import Alert, Area
from django.core.serializers import serialize
from django.http import HttpResponse
from datetime import datetime


class AlertDetailView(View):

    def get(self, request, *args, **kwargs):
        cap_slug = self.kwargs['cap_slug']
        alert = Alert.objects.get(cap_slug=cap_slug)
        try:
            filtered = [x.geom for x in Area.objects.filter(cap_info__cap_alert=alert)]
            gc = GeometryCollection(filtered)
            bounds_lng1, bounds_lat1, bounds_lng2, bounds_lat2 = gc.extent
        except:  # This might happen if the alert doesn't have geom
            bounds_lng1, bounds_lat1, bounds_lng2, bounds_lat2 = 0, 0, 0, 0

        return render(request, 'alertdb/detail.html', {'alert': alert,
                                                       'bounds_lng1': bounds_lng1, 'bounds_lat1': bounds_lat1,
                                                       'bounds_lng2': bounds_lng2, 'bounds_lat2': bounds_lat2})


class AlertListView(View):

    def get(self, request, *args, **kwargs):
        # alerts = Alert.objects.all().prefetch_related('info_set', 'info_set__area_set')
        # areas = Area.objects.all()
        areas = Area.objects.filter(cap_info__cap_expires__gte=datetime.now())
        data = serialize('geojson', areas,
                        geometry_field='geom',
                        fields=('pk'))

        return HttpResponse(data, content_type='json')
