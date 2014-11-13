from loaderio.Loaderio import Loaderio
import sys
from os import getenv
from time import sleep


api_key = getenv('LOADER_IO_KEY', None)

test_id = getenv('TEST_ID', None)

loader = Loaderio(api_key)

result_id = loader.tests.run(test_id)['result_id']

result = None

for x in range(0, 300, 10):
    sleep(10)
    result = loader.results.get(test_id,result_id)
    if result['status'] == 'ready': break

if result:
    avg_response_time = result['avg_response_time']
    if avg_response_time > 1000:
        print "[ERROR] avg_response_time (%s ms) too high" % avg_response_time
        sys.exit(1)
    else:
        print "[SUCCESS] avg_response_time (%s ms) within acceptable margins" % avg_response_time

