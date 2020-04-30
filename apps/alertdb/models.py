from django.contrib.gis.db import models
from django.contrib.gis.geos.collections import MultiPolygon, Point, Polygon
from django.contrib.auth.models import User
from django.db.models import Manager as GeoManager
from sentry_sdk import capture_exception

# Create your models here.


class Geocode(models.Model):
    GEOCODE_CHOICES = (
        ('FIPS6', 'FIPS6'),
        ('Taiwan_Geocode_100', 'Taiwan Townships'),
        ('SAME', 'SAME')
    )

    name = models.CharField(max_length=200, blank=True, null=True)  # corresponds to the 'str' field
    nativename = models.CharField(max_length=200, blank=True, null=True)
    code = models.CharField(max_length=200, blank=True, null=True)
    value_name = models.CharField(max_length=50, blank=True, null=True, choices=GEOCODE_CHOICES)

    geom = models.MultiPolygonField(srid=4326)
    objects = GeoManager()

    def __unicode__(self):              # __unicode__ on Python 2
        return 'Name: %s' % self.name


class Alert(models.Model):
    STATUS_CHOICES = (
        ('Actual', 'Actual'),
        ('System', 'System'),
        ('Exercise', 'Exercise'),
        ('Test', 'Test'),
        ('Draft', 'Draft'),
    )

    MESSAGE_TYPE_CHOICES = (
        ('Alert', 'Alert'),
        ('Update', 'Update'),
        ('Cancel', 'Cancel'),
        ('Ack', 'Ack'),
        ('Error', 'Error'),
    )

    SCOPE_CHOICES = (
        ('Public', 'Public'),
        ('Restricted', 'Restricted'),
        ('Private', 'Private'),
    )

    cap_id = models.CharField(max_length=500, unique=True, blank=True, null=True)
    cap_slug = models.CharField(max_length=50, blank=True, null=True)  # just in case cap_id is not useable
    cap_sender = models.CharField(db_index=True, max_length=200, blank=True, null=True)
    cap_sent = models.DateTimeField(db_index=True, blank=True, null=True)
    cap_status = models.CharField(max_length=10, choices=STATUS_CHOICES, blank=True, null=True)
    cap_message_type = models.CharField(max_length=10, choices=MESSAGE_TYPE_CHOICES, blank=True, null=True)
    cap_source = models.CharField(max_length=500, blank=True, null=True)
    cap_scope = models.CharField(max_length=15, choices=SCOPE_CHOICES, blank=True, null=True)
    cap_restriction = models.TextField(blank=True, null=True)
    cap_addresses = models.CharField(max_length=500, blank=True, null=True)
    cap_code = models.CharField(max_length=500, blank=True, null=True)
    cap_note = models.TextField(blank=True, null=True)
    cap_references = models.TextField(blank=True, null=True)
    cap_incidents = models.CharField(max_length=500, blank=True, null=True)
    cap_date_received = models.DateTimeField(db_index=True, auto_now_add=True)
    cap_raw = models.TextField(blank=True, null=True)
    contributor = models.ForeignKey(User, editable=True, blank=True, null=True, on_delete=models.CASCADE)

    def __unicode__(self):
        if self.cap_id is not None:
            return self.cap_id


class Info(models.Model):
    CATEGORY_CHOICES = (
        ('Geo', 'Geo'),
        ('Met', 'Meteorological'),
        ('Safety', 'Safety'),
        ('Security', 'Security'),
        ('Rescue', 'Rescue'),
        ('Fire', 'Fire'),
        ('Health', 'Health'),
        ('Env', 'Env'),
        ('Transport', 'Transport'),
        ('Infra', 'Infrastructure'),
        ('CBRNE', 'CBRNE'),
        ('Other', 'Other'),
    )

    SEVERITY_CHOICES = (
        ('Extreme', 'Extreme'),
        ('Severe', 'Severe'),
        ('Moderate', 'Moderate'),
        ('Minor', 'Minor'),
        ('Unknown', 'Unknown'),
    )

    URGENCY_CHOICES = (
        ('Immediate', 'Immediate'),
        ('Expected', 'Expected'),
        ('Future', 'Future'),
        ('Past', 'Past'),
        ('Unknown', 'Unknown'),
    )

    CERTAINTY_CHOICES = (
        ('Observed', 'Observed'),
        ('Likely', 'Likely'),
        ('Possible', 'Possible'),
        ('Unlikely', 'Unlikely'),
        ('Unknown', 'Unknown'),
    )

    RESPONSE_TYPE_CHOICES = (
        ('Shelter', 'Shelter'),
        ('Evacuate', 'Evacuate'),
        ('Prepare', 'Prepare'),
        ('Execute', 'Execute'),
        ('Avoid', 'Avoid'),
        ('Monitor', 'Monitor'),
        ('Assess', 'Assess'),
        ('AllClear', 'AllClear'),
        ('None', 'None'),
    )

    cap_language = models.CharField(max_length=75, blank=True, null=True, default='')
    cap_category = models.CharField(max_length=15, choices=CATEGORY_CHOICES)
    cap_event = models.CharField(max_length=500, blank=True, null=True)
    cap_response_type = models.CharField(max_length=15, choices=RESPONSE_TYPE_CHOICES, blank=True, null=True)
    cap_urgency = models.CharField(max_length=15, choices=URGENCY_CHOICES, blank=True, null=True)
    cap_severity = models.CharField(max_length=15, choices=SEVERITY_CHOICES)
    cap_certainty = models.CharField(max_length=15, choices=CERTAINTY_CHOICES)
    cap_audience = models.CharField(max_length=500, blank=True, null=True)
    cap_event_code = models.CharField(max_length=500, blank=True, null=True)
    cap_effective = models.DateTimeField(blank=True, null=True)
    cap_onset = models.DateTimeField(blank=True, null=True)
    cap_expires = models.DateTimeField(db_index=True, blank=True, null=True)
    cap_sender_name = models.CharField(max_length=200, blank=True, null=True)
    cap_headline = models.CharField(max_length=500)
    cap_description = models.TextField()
    cap_instruction = models.TextField(blank=True, null=True)
    cap_link = models.URLField(blank=True)
    cap_contact = models.CharField(max_length=500, blank=True, null=True)
    cap_alert = models.ForeignKey(Alert, blank=True, null=True, on_delete=models.CASCADE)

    def __unicode__(self):
        if self.cap_headline is not None:
            return self.cap_headline


class Parameter(models.Model):
    value_name = models.CharField(max_length=50, blank=True, null=True)
    value = models.CharField(max_length=500, blank=True, null=True)
    cap_info = models.ForeignKey(Info, blank=True, null=True, on_delete=models.CASCADE)


class Resource(models.Model):
    cap_resource_desc = models.CharField(max_length=500, blank=True, null=True)
    cap_mime_type = models.CharField(max_length=75, blank=True, null=True)
    cap_size = models.CharField(max_length=75, blank=True, null=True)
    cap_uri = models.URLField(blank=True)
    cap_deref_rui = models.URLField(blank=True)
    cap_digest = models.CharField(max_length=75, blank=True, null=True)
    cap_info = models.ForeignKey(Info, blank=True, null=True, on_delete=models.CASCADE)


class Area(models.Model):
    area_description = models.TextField(blank=True, null=True, default='')
    geocode_list = models.TextField(blank=True, null=True)
    cap_info = models.ForeignKey(Info, blank=True, null=True, on_delete=models.CASCADE)

    # GeoDjango-specific: a geometry field (MultiPolygonField), and
    # overriding the default manager with a GeoManager instance.
    geom = models.MultiPolygonField(blank=True, null=True, srid=4326, geography=True)
    objects = GeoManager()

    def __unicode__(self):
        if self.area_description is not None:
            return self.area_description[:50]

    def geocodeToMultiPolygon(self, geocode_list, value_name):
        try:
            if value_name and geocode_list:
                result = Geocode.objects.filter(value_name=value_name, code__in=geocode_list)
                result = result.aggregate(models.Union('geom'))['geom__union']
                if result.geom_type != 'MultiPolygon':
                    self.geom = MultiPolygon(result)
                else:
                    self.geom = result
        except Exception as e:
            capture_exception(e)

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

        self.geom = MultiPolygon(s)

    def polygonToMultiPolygon(self, polygon):
        poly_split = polygon.split(' ')
        point_list = []

        for coords in poly_split:
            poly_pnts = coords.split(',')
            pnt = Point(float(poly_pnts[1]), float(poly_pnts[0]))
            point_list.append(pnt)

        p = Polygon(point_list)  # Can't convert directly from points to MultiPolygon
        self.geom = MultiPolygon(p)
