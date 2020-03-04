from src.libs.avalon_test_wrapper \
    import build_request_obj, read_json, submit_request, \
    pre_test_env
import logging
import globals
from src.work_order_get_result.work_order_get_result_params \
    import WorkOrderGetResult
from src.utilities.generic_utils import GetResultWaitTime
import time
from src.libs import constants
from src.utilities.submit_request_utility import \
    submit_request_listener
logger = logging.getLogger(__name__)


class TestBase():

    def __init__(self):
        self.uri_client = globals.uri_client
        self.build_request_output = {}

    def setup_and_build_request_lookup(self, input_file):
        pre_test_output = pre_test_env(input_file, self.uri_client)
        request_obj, action_obj = build_request_obj(input_file)
        self.build_request_output.update({'request_obj': request_obj})
        return 0

    def setup_and_build_request_wo_submit(self, input_file):
        pre_test_output = pre_test_env(input_file, self.uri_client)
        request_obj, action_obj = build_request_obj(
            input_file, pre_test_output=pre_test_output)
        self.build_request_output.update(
            {'request_obj': request_obj,
             'pre_test_output': pre_test_output,
             'action_obj': action_obj})
        return 0

    def setup_and_build_request_retrieve(self, input_file):
        pre_test_output = pre_test_env(input_file, self.uri_client)
        request_obj, action_obj = build_request_obj(
            input_file, pre_test_response=pre_test_output)
        self.build_request_output.update(
            {'request_obj': request_obj,
             'pre_test_output': pre_test_output,
             'action_obj': action_obj})
        return 0

    def setup_and_build_request_receipt(self, input_file):
        pre_test_output, wo_submit = pre_test_env(input_file, self.uri_client)
        request_obj, action_obj = build_request_obj(
            input_file, pre_test_output=pre_test_output,
            pre_test_response=wo_submit)
        self.build_request_output.update(
            {'request_obj': request_obj,
             'pre_test_output': pre_test_output,
             'action_obj': action_obj})
        return 0

    def teardown(self):
        logger.info("**No Teardown Defined**\n%s\n")

    def getresult(self, output_obj):
        if constants.direct_test_mode == "listener":
            work_order_id = output_obj["params"]["workOrderId"]
            request_id = output_obj["id"] + 1
        else:
            request_id = 12
            work_order_id = output_obj.get_work_order_id()
        getresult_obj = WorkOrderGetResult()
        output_obj_getresult = getresult_obj.configure_data(
            request_id, work_order_id)
        logger.info("----- Validating WorkOrderGetResult Response ------")
        response = {}

        response_timeout_start = time.time()
        response_timeout_multiplier = ((6000 / 3600) + 6) * 3
        while "result" not in response:
            if "error" in response:
                if response["error"]["code"] != 5:
                    logger.info('WorkOrderGetResult - '
                                'Response received with error code. ')
                    err_cd = 1
                    break

            response_timeout_end = time.time()
            if ((response_timeout_end - response_timeout_start) >
                    response_timeout_multiplier):
                logger.info('ERROR: WorkOrderGetResult response is not \
                                   received within expected time.')
                break

            # submit work order get result request and retrieve response
            response = submit_request_listener(
                self.uri_client, output_obj_getresult,
                constants.wo_result_output_json_file_name)
            time.sleep(GetResultWaitTime.LOOP_WAIT_TIME.value)
            logger.info("******Received Response*****\n%s\n", response)
        return response
