from django.contrib.gis import admin
from apps.alertdb.models import Alert, Info, Area, Parameter, Resource
from apps.alertdb.models import Geocode

# Register your models here.


class GeocodeAdmin(admin.GeoModelAdmin):
    list_display = ('name', 'code', 'nativename',)
    search_fields = ['code']
    openlayers_url = '//cdnjs.cloudflare.com/ajax/libs/openlayers/2.13.1/OpenLayers.js'
    wms_url = 'http://irs.gis-lab.info'
    wms_layer = 'osm'
admin.site.register(Geocode, GeocodeAdmin)


class AreaAdmin(admin.GeoModelAdmin):
    def __init__(self, *args, **kwargs):
        super(AreaAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = (None, )


    search_fields = ['area_description']
    readonly_fields = ['cap_info']
    list_display = ('area_link',)
    openlayers_url = '//cdnjs.cloudflare.com/ajax/libs/openlayers/2.13.1/OpenLayers.js'
    wms_url = 'http://irs.gis-lab.info'
    wms_layer = 'osm'

    def area_link(self, obj):
        if obj.area_description is not None:
            short_tag = obj.area_description[:60]
        else:
            short_tag = "Area ID #%s" % obj.id
        return u'<a href="/admin/alertdb/area/%s/">%s</a>' % (obj.id, short_tag)

    area_link.allow_tags = True
    area_link.short_description = "Area Name"
admin.site.register(Area, AreaAdmin)


class ParameterAdmin(admin.GeoModelAdmin):
    list_display = ('value_name', 'value')
    readonly_fields = ['cap_info']
admin.site.register(Parameter, ParameterAdmin)


class ResourceAdmin(admin.GeoModelAdmin):
    list_display = ('cap_resource_desc', 'cap_mime_type')
    readonly_fields = ['cap_info']
admin.site.register(Resource, ResourceAdmin)


class InfoAdmin(admin.GeoModelAdmin):
    search_fields = ['cap_description']
    readonly_fields = ['cap_alert']
    list_display = ('cap_effective', 'cap_event_code', 'cap_category', 'cap_severity', 'cap_certainty')
admin.site.register(Info, InfoAdmin)


class AlertAdmin(admin.GeoModelAdmin):
    list_filter = ('cap_scope', 'cap_sender',)
    search_fields = ['cap_description']
    list_display = ('cap_date_received', 'cap_sender', 'cap_status',)
admin.site.register(Alert, AlertAdmin)
