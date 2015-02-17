from loaderio.Loaderio import Loaderio
import sys
from os import getenv
from time import sleep


api_key = getenv('LOADER_IO_KEY', None)

test_id = getenv('TEST_ID', None)
test_id_2 = getenv('TEST_ID_2', None)

loader = Loaderio(api_key)

result_id = loader.tests.run(test_id)['result_id']
result_id_2 = loader.tests.run(test_id_2)['result_id']

result = None
result_2 = None

for x in range(0, 300, 10):
    sleep(10)
    result = loader.results.get(test_id,result_id)
    result_2 = loader.results.get(test_id,result_id_2)
    if result['status'] == 'ready' and result_2 == 'ready': break

if result and result_2:
    if result['avg_response_time'] > 1000 < result_2['avg_response_time']:
        print "[ERROR] Average test time from Loader too high"
        sys.exit(1)
    else:
        print "[SUCCESS] Average test time from Loader within acceptable margins"

