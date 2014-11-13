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
    if result['avg_response_time'] > 1000:
        print "[ERROR] avg_response_time too higher"
        sys.exit(1)
    else:
        print "[SUCCESS] avg_response_time within acceptable margins"

