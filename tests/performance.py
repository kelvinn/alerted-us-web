from loaderio.Loaderio import Loaderio
import sys
from os import getenv
from time import sleep


API_KEY = getenv('LOADER_IO_KEY', None)
TEST_ID = getenv('TEST_ID', None)
TEST_ID_2 = getenv('TEST_ID_2', None)

loader = Loaderio(API_KEY)

def run_tests(test_id):
    result = None
    pending_result_id = loader.tests.run(test_id)
    if pending_result_id['message'] == 'success':
        sleep(60) # The tests are 60 seconds, so we know to sleep at least this long
        for x in range(0, 300, 10): # TODO This should be refactored to be more reliable, I think the APi has issues
            sleep(10)
            print("going...")
            result = loader.results.get(test_id, pending_result_id['result_id'])
            if result['status'] == 'ready': break

        print(result)
        try:
            avg_response_time = result['avg_response_time']
            if 1000 < avg_response_time:
                print("[ERROR] Average too high (%sms)" % avg_response_time)
                sys.exit(1)
            else:
                print("[SUCCESS] Average test time within acceptable margins %sms" % avg_response_time)
        except:
            print("[ERROR] Average response time not provided from Loader.io")
    else:
        print("[ERROR] Loader.io says: %s" % pending_result_id['errors'])

if __name__ == '__main__':
    run_tests(TEST_ID)
    run_tests(TEST_ID_2)