from __future__ import absolute_import

from celery import shared_task
from django.core.serializers import json
from apps.alertdb.models import Info
from apps.people.models import Notification, LocationHistory
from apps.alertdb.tasks import publish_to_device
from statsd.defaults.django import statsd


class CleanSerializer(json.Serializer):
    def get_dump_object(self, obj):
        return self._current


@shared_task
def save_location_history(loc_instance):
    """

    :param loc_instance:
    """
    timer = statsd.timer('task.save_location_history')
    timer.start()
    location = LocationHistory()
    location.name = loc_instance.name
    location.user = loc_instance.user
    location.date_received = loc_instance.date_received
    location.geom = loc_instance.geom
    location.save()
    statsd.incr('task.save_location_history')
    timer.stop()
    return True


@shared_task
def run_alertdb_search(loc_instance):
    """

    :param loc_instance:
    """
    timer = statsd.timer('task.run_alertdb_search')
    timer.start()
    try:

        # Current problems with this include alerting to test alerts, and if a single alert has multiple info fields
        # for the same alert, e.g. for language
        info_list = Info.objects.filter(
            cap_expires__gte=loc_instance.date_received
        ).filter(
            area__geom__intersects=loc_instance.geom
        ).exclude(
            notification__user=loc_instance.user
        )

        for info in info_list:
            notif = Notification(cap_info=info, user=loc_instance.user)
            serializer = CleanSerializer()
            array_result = serializer.serialize([info])
            just_object_result = array_result[1:-1]
            notif.message_id = 1
            notif.save()
            publish_to_device.delay(just_object_result, loc_instance.user)
        statsd.incr('task.run_alertdb_search')

    except Exception:
        pass
    timer.stop()
    return True
