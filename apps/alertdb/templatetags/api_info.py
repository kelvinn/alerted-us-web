from django import template
from apps.alertdb.models import Info, Alert

register = template.Library()

@register.inclusion_tag('admin/alertdb/alert/infos.html')
def display_infos(entry_id):
    alert_obj = Alert.objects.get(id__exact=entry_id)
    infos = Info.objects.filter(cap_alert=alert_obj)
    return { 'infos': infos }