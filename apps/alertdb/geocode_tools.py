
"""
You load shapes like this:

from apps.alertdb.geocode_tools import GeocodeLoader
g = GeocodeLoader()
g.run_taiwan()  # Sample dataset only (100 entries). Will download 100MB file.
g.run_taiwan(sample=False)  # This loads the entire shapefile
g.run_fips6(sample=False)
g.run_philippines(sample=False)
"""

import os
import sys
import gc
import logging
import tempfile
try:
    from urllib.request import urlopen
    from urllib.error import URLError, HTTPError
except ImportError:
    from urllib2 import urlopen
import zipfile
from time import sleep
import socket

# First, add the project to PATH
PWD = os.path.dirname(os.path.abspath(__file__))
PROJECT_PATH = os.path.abspath(os.path.join(PWD, '../../'))
sys.path.append(PROJECT_PATH)

# Second, configure this script to use Django
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

try:
    django.setup()  # Removing this halts celery in Django 1.7
except AttributeError:
    print(django.VERSION)

# Third, import the needed Django stuff
from django.contrib.gis.utils import LayerMapping
from django.contrib.gis.geos.collections import MultiPolygon
from apps.alertdb.models import Geocode

FIPS6_MAPPING = {
    'name': 'COUNTYNAME',
    'code': 'FIPS',
    'geom': 'MULTIPOLYGON',
}

TW_TOWNSHIP_MAPPING = {
    'name': 'ENG_NAME',
    'nativename': 'D_NAME',
    'code': 'nTOWN',
    'geom': 'MULTIPOLYGON',
}

PH_MAPPING = {
    'name': 'PROVINCE',
    'code': 'PSGC',
    'geom': 'MULTIPOLYGON',
}

def queryset_iterator(queryset, chunksize=250):
    """
    Iterate over a Django Queryset ordered by the primary key

    This method loads a maximum of chunksize (default: 1000) rows in it's
    memory at the same time while django normally would load all rows in it's
    memory. Using the iterator() method only causes it to not preload all the
    classes.

    Note that the implementation of the iterator does not support ordered query sets.
    """
    pk = 0
    last_pk = queryset.order_by('-pk')[0].pk
    queryset = queryset.order_by('pk')
    while pk < last_pk:
        for row in queryset.filter(pk__gt=pk)[:chunksize]:
            pk = row.pk
            yield row
        gc.collect()


def dlfile(temp_directory, shape_zip_file_name):
    # Open the url
    url = "https://d2382d6dswfsst.cloudfront.net/cozysiren/%s" % shape_zip_file_name
    full_file_path = temp_directory + "/" + shape_zip_file_name

    try:
        f = urlopen(url) # Try running "sudo ./Install\ Certificates.command" on Mac OS X if this doesn't work
        print("downloading " + url)

        # Open our local file for writing
        with open(full_file_path, "wb") as local_file:
            local_file.write(f.read())

    # Handle possible errors
    except HTTPError:
        print("HTTP Error:", url)
    except URLError:
        print("URL Error:", url)


class GeocodeLoader():
    def __init__(self):
        self.shape_file_name = None
        self.shape_mappings = None
        self.value_name = None
        self.dirpath = tempfile.mkdtemp()

    def start(self):
        # This file is populated from here:
        # http://www.nws.noaa.gov/geodata/catalog/county/html/county.htm

        filepath = self.dirpath + "/" + self.shape_zip_file_name
        if not os.path.isfile(filepath):
            dlfile(self.dirpath, self.shape_zip_file_name)
            with zipfile.ZipFile(filepath, "r") as z:
                z.extractall(self.dirpath)

        print("Finished downloading data")
        self.load_data()

    def load_data(self):

        # First erase any existing Geocodes with the same value_name
        print("Erasing Geocodes with value_name %s" % self.value_name)
        Geocode.objects.filter(value_name=self.value_name).delete()

        print("Erasing any Geocodes with None as value_name")
        Geocode.objects.filter(value_name=None).delete()

        print("Loading new Geocodes")
        shp_name = os.path.abspath(os.path.join(self.dirpath, self.shape_file_name))
        lm = LayerMapping(Geocode, shp_name, self.shape_mappings,
                          transform=True, encoding=self.shape_encoding)

        # We load only the first 100 FIPS objects if it is a sample
        if self.sample is True:
            lm.save(strict=True, verbose=False, fid_range=[0, 100])
        else:
            lm.save(strict=True, verbose=False)

        print("Post-processing Geocodes")

        # We use this queryset_iterator function so not all objects are loaded in memory at the same time
        result = queryset_iterator(Geocode.objects.filter(value_name=None))

        z = 0  # Counter to print

        # We need to do some post processing on the geocodes, e.g. convert to MultiPolygon and remove 0s
        for i in result:
            z += 1
            try:

                print("%s %s" % (z, i.name))

                # this is to add just a little room between the lines
                g = i.geom.buffer(-0.0000001)

                # Simplify the polygons and convert to multipolygon
                g = g.simplify(0.04, preserve_topology=True)
                if g.geom_type != 'MultiPolygon':
                    i.geom = MultiPolygon(g)
                else:
                    i.geom = g

                # Remove leading zeros. Leading zeros pose problems when matching up with requests
                i.code = i.code.lstrip("0")

                # Set value_name, e.g. FIPS6
                i.value_name = self.value_name
                i.save()
                sleep(0.05)  # We do this to give the DB a second to catch its breath

            except Exception:
                logging.error("error processing geocodes")

        print("Finished loading data")

    def run_fips6(self, sample=True):
        self.shape_mappings = FIPS6_MAPPING
        self.shape_file_name = "c_01ap14.shp"
        self.shape_zip_file_name = "c_01ap14a.zip"
        self.shape_encoding = 'iso-8859-1'
        self.value_name = 'FIPS6'
        self.sample = sample
        self.start()
        return True

    def run_taiwan(self, sample=True):
        self.shape_mappings = TW_TOWNSHIP_MAPPING
        self.shape_file_name = "taiwan_utf8.shp"
        self.shape_zip_file_name = "taiwan_utf8.zip"
        self.shape_encoding = 'utf-8'
        self.value_name = 'Taiwan_Geocode_100'
        self.sample = sample
        self.start()
        return True

    def run_philippines(self, sample=True):
        self.shape_mappings = PH_MAPPING
        self.shape_file_name = "provinces.shp"
        self.shape_zip_file_name = "ph_provinces.zip"
        self.shape_encoding = 'utf-8'
        self.value_name = 'SAME'
        self.sample = sample
        self.start()


def main():
    if 'RACK_ENV' in os.environ:
        if os.environ['RACK_ENV'] == "development" or os.environ['RACK_ENV'] == "staging":
            g = GeocodeLoader()
            g.run_taiwan()
            g.run_fips6()
            g.run_philippines()
            return True
    else:
        raise Exception('Not allowed to load sample data outside DEV')


if __name__ == "__main__":
    main()
