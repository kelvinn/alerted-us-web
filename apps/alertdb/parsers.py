import dateutil.parser as dparser
from rest_framework.parsers import BaseParser
from rest_framework.exceptions import ParseError
from django.contrib.gis.geos.collections import MultiPolygon, Point, Polygon
from django.contrib.gis.db.models import Union
from capparselib.parsers import CAPParser
from statsd.defaults.django import statsd
import random
import logging
from apps.alertdb.models import Geocode

SIMPLE_CAP_TYPES = [
    'cap_response_type',
    'cap_expires',
    'cap_status',
    'cap_restriction',
    'cap_event',
    'cap_urgency',
    'cap_contact',
    'cap_effective',
    'cap_description',
    'cap_id',
    'cap_link',
    'cap_code',
    'cap_sender',
    'cap_note',
    'cap_incidents',
    'cap_addresses',
    'cap_source',
    'cap_references',
    'cap_severity',
    'cap_sent',
    'cap_scope',
    'cap_certainty',
    'cap_category',
    'cap_headline',
    'cap_language',
    'cap_alert_type',
    'cap_instruction'
]

COMPLEX_CAP_TYPES = [
    'cap_info',
]

DATETIME_CAP_TYPE = [
    'cap_effective',
    'cap_onset',
    'cap_sent',
    'cap_expires',
]


class CAPXMLParser(BaseParser):
    """
    Django Rest Framework customer parser for Common Alerting Protocol feeds, to be used in conjuction with the
    capparselib library, which standardises the different CAP versions into a normal python dictionary.
    """

    media_type = '*/xml'

    def format(self):
        return None

    def geocodeToMultiPolygon(self, geocode_list, value_name):
        try:

            result = Geocode.objects.filter(value_name=value_name, code__in=geocode_list)
            if len(result) > 0:
                result = result.aggregate(Union('geom'))['geom__union']
                try:
                    if result.geom_type != 'MultiPolygon':
                        geom = MultiPolygon(result)
                    else:
                        geom = result
                except Exception,e:
                    logging.error('Error in geocodeToMultiPolygon')
                    geom = None
                return geom
            else:
                return None
        except Exception, e:
            print e

    def circleToMultiPolygon(self, circle):
        # circle is usually of the form '-35.3888,147.0598 25.0', so the below should make sense
        circle_split = circle.split(' ')
        coords = circle_split[0].split(',')
        p = Point(float(coords[1]), float(coords[0]))

        circle_rad = float(circle_split[1])
        if circle_rad < 3:
            circle_rad = 3.0  # This is to allow some level of smoothing
        rdn = circle_rad / 6371

        x = p.buffer(rdn)
        s = x.simplify(rdn / 3.5, preserve_topology=False)

        geom = MultiPolygon(s)
        return geom

    def polygonToMultiPolygon(self, polygon):
        poly_split = polygon.split(' ')
        point_list = []

        for coords in poly_split:
            poly_pnts = coords.split(',')
            pnt = Point(float(poly_pnts[1]), float(poly_pnts[0]))
            point_list.append(pnt)

        p = Polygon(point_list)  # Can't convert directly from points to MultiPolygon
        geom = MultiPolygon(p)
        return geom

    def process_item_obj(self, item_obj):
        info_obj = dict()

        for info_key, info_value in item_obj.items():
            if info_key in SIMPLE_CAP_TYPES:
                info_obj[info_key] = info_value

            #  Convert any datetime obj to datetime object
            if info_key in DATETIME_CAP_TYPE:
                try:
                    info_value = dparser.parse(str(info_value))
                    info_obj[info_key] = info_value
                except Exception, err:
                    logging.error('parsers.py incorrect format')

            if info_key == 'cap_parameter':
                parameter_list = []
                for ptr_item in info_value:
                    parameter_obj = dict()
                    parameter_obj['value_name'] = ptr_item['valueName']
                    parameter_obj['value'] = ptr_item['value']
                    parameter_obj['cap_info'] = info_obj
                    parameter_list.append(parameter_obj)
                item_obj['parameter_set'] = parameter_list

            if info_key == 'cap_resource':
                resource_list = []
                for res_item in info_value:
                    res_obj = dict()
                    res_obj['cap_resource_desc'] = res_item['resourceDesc']
                    res_obj['cap_mime_type'] = res_item['mimeType']
                    res_obj['cap_uri'] = res_item['uri']
                    res_obj['cap_info'] = info_obj
                    resource_list.append(res_obj)
                item_obj['resource_set'] = resource_list

            if info_key == 'cap_area':
                area_obj_list = []
                for area_item in info_value:

                    area_obj = dict()
                    area_obj['area_description'] = area_item['area_description']
                    if 'circle' in area_item:
                        circle = str(area_item['circle'])
                        if len(circle) > 5:  # CAPs sometimes have empty polygon tags
                            area_obj['geom'] = self.circleToMultiPolygon(circle)

                    if 'polygon' in area_item:
                        polygon = str(area_item['polygon'])
                        if len(polygon) > 5:  # CAPs sometimes have empty polygon tags
                            area_obj['geom'] = self.polygonToMultiPolygon(polygon)

                    if 'geocodes' in area_item:  # TODO still some cleaning to do
                        geocode_list = []
                        value_name_save = None
                        for geocode in area_item['geocodes']:
                            value_name = geocode['valueName']
                            if value_name == 'FIPS6' or value_name == 'Taiwan_Geocode_100':
                                geocode_list.append(str(geocode['value']))
                                value_name_save = value_name

                        if len(geocode_list) > 0:
                            logging.info("Looking up MultiPolygon with value_name %s" % value_name_save)
                            geom = self.geocodeToMultiPolygon(geocode_list, value_name_save)
                            if geom:  # This is mainly for t esting, as it will likely not have a geom
                                area_obj['geom'] = geom
                            area_obj['geocode_list'] = geocode_list
                        else:
                            logging.error("No value_name")

                    area_obj_list.append(area_obj)
                info_obj['area_set'] = area_obj_list
        return info_obj

    @statsd.timer('api.CAPXMLParser.parse')
    def parse(self, stream, media_type=None, parser_context=None):
        """
        Simply return a string representing the body of the request.
        """
        body_text = stream.read()
        data = []
        try:
            alerts = CAPParser(body_text).as_dict()
        except:
            statsd.incr('api.CAPXMLParser.parse')
            logging.error("CAPParser Invalid XML")
            raise ParseError

        for alert in alerts:
            alert_obj = dict()
            alert_obj['cap_raw'] = body_text

            cap_slug = '%030x' % random.randrange(16**30)
            alert_obj['cap_slug'] = cap_slug

            for alert_key, alert_value in alert.items():
                if alert_key in SIMPLE_CAP_TYPES:
                    if 'cap_sent' == alert_key:
                        alert_value = dparser.parse(str(alert_value))
                    alert_obj[alert_key] = alert_value

                elif alert_key == 'cap_info':
                    item_obj_list = []
                    for item_obj in alert['cap_info']:
                        # TODO run as background task
                        processed = self.process_item_obj(item_obj)
                        item_obj_list.append(processed)
                    alert_obj['info_set'] = item_obj_list
            data.append(alert_obj)

        return data