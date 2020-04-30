__author__ = 'kelvin'

from os import getenv
import base64
import requests
import random


# Don't forget to set with "python manage.py createsuperuser --username "

if getenv('ALERTED_USERPASS'):
    ALERTED_API = str(getenv('ALERTED_API'))
    ALERTED_USERPASS = str(getenv('ALERTED_USERPASS'))
else:
    ALERTED_API = 'http://localhost:8000/api/v1/alerts/'
    ALERTED_USERPASS = 'admin:password'  # This is the same default password used in the dev alerted website

HEADERS = {'Content-Type': 'application/xml',
           'Authorization': 'Basic %s' % base64.b64encode(str(ALERTED_USERPASS).encode())}

FIPSLIST = [u'15009', u'72119', u'72011', u'72021', u'72087', u'66010', u'72015', u'72017', u'72019', u'69085',
            u'69110', u'69120', u'72025', u'72029', u'72047', u'9003', u'9015', u'24023', u'24021', u'24031',
            u'72037', u'72039', u'72054', u'72055', u'72043', u'72045', u'72059', u'72061', u'72063', u'72065',
            u'72097', u'72073', u'72075', u'72077', u'72101', u'72081', u'72085', u'72091', u'72093', u'72099',
            u'72105', u'72107', u'72109', u'72113', u'72121', u'72125', u'72127', u'72129', u'72139', u'72141',
            u'72131', u'72143', u'72149', u'72031', u'72153', u'72001', u'72007', u'72009', u'78010', u'72013',
            u'9013', u'72117', u'72071', u'72027', u'72051', u'72135', u'72003', u'72023', u'15007', u'69100',
            u'72033', u'72089', u'72069', u'78020', u'60050', u'60010', u'72035', u'72041', u'25019', u'72111',
            u'60040', u'60020', u'24043', u'24017', u'72057', u'72067', u'72103', u'72123', u'72079', u'72095',
            u'72133', u'72151', u'72083', u'72005', u'72049', u'72053', u'72147', u'78030', u'72115', u'15001']


def generate_text():
    txt = """
            <?xml version = '1.0' encoding = 'UTF-8' standalone = 'yes'?>
            <?xml-stylesheet href='http://alerts.weather.gov/cap/capatomproduct.xsl' type='text/xsl'?>

            <!--
            This atom/xml feed is an index to active advisories, watches and warnings
            issued by the National Weather Service.  This index file is not the complete
            Common Alerting Protocol (CAP) alert message.  To obtain the complete CAP
            alert, please follow the links for each entry in this index.  Also note the
            CAP message uses a style sheet to convey the information in a human readable
            format.  Please view the source of the CAP message to see the complete data
            set.  Not all information in the CAP message is contained in this index of
            active alerts.
            -->

            <alert xmlns = 'urn:oasis:names:tc:emergency:cap:1.1'>

            <!-- http-date = Sun, 11 May 2014 04:00:00 GMT -->
            <identifier>%s</identifier>
            <sender>w-nws.webmaster@noaa.gov</sender>
            <sent>2014-05-10T22:00:00-06:00</sent>
            <status>Actual</status>
            <msgType>Alert</msgType>
            <scope>Public</scope>
            <note>Test note</note>
            <info>
            <category>Met</category>
            <event>Wind Advisory</event>
            <urgency>Expected</urgency>
            <severity>Minor</severity>
            <certainty>Likely</certainty>
            <eventCode>
            <valueName>SAME</valueName>
            <value></value>
            </eventCode>
            <effective>2014-05-10T22:00:00-06:00</effective>
            <expires>2016-05-11T19:00:00-06:00</expires>
            <senderName>NWS Albuquerque (Northern and Central New Mexico)</senderName>
            <headline>Wind Advisory issued May 10 at 10:00PM MDT until May 11 at 7:00PM MDT by NWS Albuquerque</headline>
            <description>Test Description</description>
            <instruction>MOTORISTS SHOULD EXERCISE CAUTION WHILE TRAVELLING. SUDDEN GUSTS
            OF WIND MAY CAUSE YOU TO LOSE CONTROL OF YOUR VEHICLE. EXTRA
            ATTENTION SHOULD BE GIVEN TO CROSS WINDS.</instruction>
            <parameter>
            <valueName>WMOHEADER</valueName>
            <value></value>
            </parameter>
            <parameter>
            <valueName>UGC</valueName>
            <value>NMZ501>507-509>520-522-528-531>540</value>
            </parameter>
            <parameter>
            <valueName>VTEC</valueName>
            <value>/O.CON.KABQ.WI.Y.0032.140511T1600Z-140512T0100Z/</value>
            </parameter>
            <parameter>
            <valueName>TIME...MOT...LOC</valueName>
            <value></value>
            </parameter>
            <area>
            <areaDesc>This is a sample description from weather.cap - FIPS codes were input to match sample FIPS codes in sample_data.json</areaDesc>
            <polygon></polygon>
            <geocode>
            <valueName>FIPS6</valueName>
            <value>%s</value>
            </geocode>
            </area>
            </info>
            </alert>
            """ % (random.randint(1, 10000000000), random.choice(FIPSLIST))
    return txt


def generate_alerts():
    alert = generate_text()
    transmit(alert)


def transmit(alert):
    """
    A function to transmit XML to Alerted web service

    :param alert: XML CAP1.2 alert to transmit
    :return:
    """
    alert = alert.replace('\n', '')
    # Determine if the alert can be parsed as valid CAP XML
    result = False

    resp = requests.post(url=ALERTED_API, data=alert, headers=HEADERS, verify=False)

    if resp.status_code == 201:
        print("Success")
        result = True
    else:
        print("ERROR")

    return result


if __name__ == "__main__":
    generate_alerts()
