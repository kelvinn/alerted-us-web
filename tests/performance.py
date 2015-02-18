from loaderio.Loaderio import Loaderio
import sys
from os import getenv
from time import sleep


api_key = getenv('LOADER_IO_KEY', None)

loader = Loaderio(api_key)


def run_tests(test_id, test_name):
    result = None
    pending_result_id = loader.tests.run(test_id)
    if pending_result_id['message'] == 'success':
        sleep(60) # The tests are 60 seconds, so we know to sleep at least this long
        for x in range(0, 300, 10): # TODO This should be refactored to be more reliable, I think the APi has issues
            sleep(10)
            result = loader.results.get(test_id, pending_result_id['result_id'])
            if result['status'] == 'ready': break

        try:
            avg_response_time = result['avg_response_time']
            if 1000 < avg_response_time:
                print "[ERROR] Average too high (%s: %sms)" % (test_name, avg_response_time)
                sys.exit(1)
            else:
                print "[SUCCESS] Average test time within acceptable margins (%s: %sms)" % (test_name, avg_response_time)
        except:
            print "[ERROR] Average response time not provided from Loader.io (%s)" % test_name
    else:
        print "[ERROR] Loader.io says for test %s: %s" % (test_name, pending_result_id['errors'])

if __name__ == '__main__':
    for loader_test in loader.tests.list():
        run_tests(loader_test['test_id'], loader_test['name'])