from django import template
from apps.alertdb.models import Info, Area

register = template.Library()


@register.inclusion_tag('admin/alertdb/info/areas.html')
def display_areas(info_id):
    cap_info = Info.objects.get(id__exact=info_id)
    areas = Area.objects.filter(cap_info=cap_info)
    return { 'areas': areas }