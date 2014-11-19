from __future__ import absolute_import

import logging
from celery import shared_task
from django.db.models import Q
from django.core.serializers import json
from django.contrib.gis.measure import D
from apps.alertdb.models import Alert
from apps.people.models import Notification, Location
from statsd.defaults.django import statsd
from push_notifications.models import GCMDevice

import gpolyencode


class CleanSerializer(json.Serializer):
    def get_dump_object(self, obj):
        return self._current


@shared_task
def publish_to_device(message, user):
    """

    :param message:
    :param user:
    """
    timer = statsd.timer('task.publish_to_device')
    timer.start()
    devices = GCMDevice.objects.filter(user=user)
    if devices:
        devices.send_message(message)
    timer.stop()


def create_map_url(info):  # TODO finish this
    try:
        encoder = gpolyencode.GPolyEncoder()
        for area in info.area_set.all():
            if area.geom:  # We do this to prevent tests from bombing out...
                image_url = None

                latlng = []
                for poly in area.geom.simplify(0.001, preserve_topology=True):
                    for x, y in poly.coords[0]:
                        latlng.append((round(x, 4), round(y, 4)))
                enc = encoder.encode(latlng)
                enc = enc['points']
                image_url = "http://maps.googleapis.com/maps/api/staticmap?size=610x340&" \
                            "maptype=roadmap&path=fillcolor:0xAA000033%7Ccolor:0xFFFFFF00%7Cenc:{0:s}&"\
                            "&scale=2&sensor=false".format(enc)
    except:
        logging.error("Error in create_map_url")


@shared_task
def run_location_search(alert_id):
    """

    :param alert_id:
    """
    timer = statsd.timer('task.run_location_search')
    timer.start()
    try:
        alert = Alert.objects.get(id=alert_id)
        for info in alert.info_set.all():
            for area in info.area_set.all():  # TODO Can this be wrapped into one query?
                if area.geom:  # We do this to prevent tests from bombing out...

                    locations = Location.objects.filter(
                        (Q(source__exact='static') & Q(geom__distance_lt=(area.geom, D(mi=3)))) |
                        (Q(source__exact='current') & Q(geom__distance_lt=(area.geom, D(mi=3))))
                    )

                    for loc in locations:
                        cap_info = area.cap_info
                        notif = Notification(cap_info=cap_info, user=loc.user)
                        notif.message_id = 1
                        notif.save()

                        # Now send alert
                        serializer = CleanSerializer()
                        array_result = serializer.serialize([cap_info])
                        just_object_result = array_result[1:-1]
                        publish_to_device.delay(just_object_result, loc.user)
        statsd.incr('task.run_location_search')
        timer.stop()
    except Exception:
        pass  # log some exception here...

