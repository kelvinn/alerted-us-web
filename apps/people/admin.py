from django.contrib.gis import admin
from django.conf import settings
from apps.people.models import Location, Notification, LocationHistory


# Register your models here.


class LocationAdmin(admin.GeoModelAdmin):
    list_display = ('date_received', 'name', 'user', 'source')
    search_fields = ['user', ]
    openlayers_url = '//cdnjs.cloudflare.com/ajax/libs/openlayers/2.13.1/OpenLayers.js'
    wms_url = 'http://irs.gis-lab.info'
    wms_layer = 'osm'
    #readonly_fields = ('geom',)
admin.site.register(Location, LocationAdmin)


class LocationHistoryAdmin(admin.GeoModelAdmin):
    list_display = ('date_received', 'name', 'user', )
    search_fields = ['user', ]
    openlayers_url = '//cdnjs.cloudflare.com/ajax/libs/openlayers/2.13.1/OpenLayers.js'
    wms_url = 'http://irs.gis-lab.info'
    wms_layer = 'osm'
    #readonly_fields = ('geom',)
admin.site.register(LocationHistory, LocationHistoryAdmin)


class NotificationAdmin(admin.GeoModelAdmin):
    list_display = ('date_created', 'user')
    if not settings.DEBUG:  # This prevents the admin from crashing with so many infos
        readonly_fields = ('cap_info', )
admin.site.register(Notification, NotificationAdmin)

