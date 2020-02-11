import json
import logging
from src.libs import constants
import crypto_utils.crypto_utility as enclave_helper
from src.worker_lookup.worker_lookup_params \
    import WorkerLookUp
from src.worker_retrieve.worker_retrieve_params \
    import WorkerRetrieve
from src.utilities.submit_request_utility import \
    submit_request, submit_work_order, \
    submit_worker_actions, submit_work_order_get_result
import avalon_client_sdk.worker.worker_details as worker
from avalon_client_sdk.utility.tcf_types import WorkerType
import crypto_utils.crypto_utility as crypto_utils

logger = logging.getLogger(__name__)


def read_json(request_file):
    # Read the method name from JSON file
    with open(request_file, "r") as file:
        input_json = file.read().rstrip('\n')

    input_json_obj = json.loads(input_json)

    return input_json_obj


def worker_retrieve(uri_client):

    worker_obj = worker.SGXWorkerDetails()

    """ Function for computing worker lookup and retrieve once per session. """

    if not uri_client:
        logger.error("Server URI is not provided")
        exit(1)

    # logger.info("Execute work order")
    response = None

    err_cd = 0
    # create worker lookup request
    output_json_file_name = 'worker_lookup'

    lookup_obj = WorkerLookUp()
    lookup_obj.set_worker_type(WorkerType.TEE_SGX.value)
    input_worker_look_up = json.loads(lookup_obj.to_string())

    # input_json_str = input_worker_look_up
    logger.info("------------------Testing WorkerLookUp------------------")

    # submit worker lookup request and retrieve response
    logger.info("********Received Request*******\n%s\n", input_worker_look_up)
    response = submit_request(uri_client, input_worker_look_up,
                              output_json_file_name)
    logger.info("**********Received Response*********\n%s\n", response)

    # check worker lookup response
    if "result" in response and "totalCount" in response["result"].keys():
        if response["result"]["totalCount"] == 0:
            err_cd = 1
            logger.info('ERROR: Failed at WorkerLookUp - \
            No Workers exist to submit workorder.')

    if err_cd == 0:

        retrieve_obj = WorkerRetrieve()

        logger.info("-----Testing WorkerRetrieve-----")
        # Retrieving the worker id from the "WorkerLookUp" response and
        # update the worker id information for the further json requests
        if "result" in response and "ids" in response["result"].keys():
            retrieve_obj.set_worker_id(crypto_utils.strip_begin_end_public_key
                                       (response["result"]["ids"][0]))
            input_worker_retrieve = json.loads(retrieve_obj.to_string())
            logger.info('*****Worker details Updated with Worker ID***** \
                           \n%s\n', input_worker_retrieve)
        else:
            logger.info('ERROR: Failed at WorkerLookUp - \
                       No Worker ids in WorkerLookUp response.')
            err_cd = 1

        if err_cd == 0:
            # submit worker retrieve request and load to worker object
            response = submit_request(uri_client, input_worker_retrieve,
                                      output_json_file_name)
            worker_obj.load_worker(response)

    return worker_obj, err_cd


def run_test(input_json_obj, setup_config):

    uri_client = setup_config
    input_method = input_json_obj["method"]

    # private_key of client
    private_key = enclave_helper.generate_signing_keys()

    # Initializing worker object to pass client default worker
    # data to testcases
    worker_obj, err_cd = worker_retrieve(uri_client)

    if input_method == "WorkOrderSubmit":
        """
        worker_obj :  Worker object to submit the work order request.
        private_key : Private key used to submit the request.
        err_cd : Status of previous request (worker retrieve), Success or Fail.
        """
        if constants.direct_test_mode == "listener":

            (err_cd, work_order_submit_response,
             final_json_str, work_order_obj) = submit_work_order(
                input_json_obj, uri_client,
                worker_obj, private_key, err_cd)

        else:
            # Create work order using client SDK

            logger.info("Code for work order submission using SDK\n")

            '''wo_params = _create_work_order_params(
                worker_obj.worker_id, input_request["params"]["workloadId"],
                input_request["params"]["inData"],
                worker_obj.encryption_key)

            response_tup, work_order_obj = submit_work_order_client_sdk(
                wo_params, input_request["id"])

            get_result_id = input_request["id"] + 1

            get_work_order_result(work_order_obj, wo_params, get_result_id)'''

        work_order_id = final_json_str["params"]["workOrderId"]
        request_id = final_json_str["id"] + 1

        err_cd, work_order_get_result_response, submiting_time = \
            submit_work_order_get_result(
                uri_client, err_cd, work_order_id, request_id)

        return \
            work_order_submit_response, \
            work_order_get_result_response, worker_obj, work_order_obj

    if input_method is "WorkOrderGetResult":
        """
        err_cd : Status of previous request (work order submit).
        work_order_id : Same work order id as in work order submit.
        request_id : Unique requester id.

        err_cd, work_order_id, request_id = request_tup[6:9]

        response_tup = submit_work_order_get_result(
            input_request, request_mode, tamper, output_json_file_name,
            uri_client, err_cd, work_order_id, request_id)"""

        logger.info("Code for get result flow\n")

    if input_method in ("WorkerUpdate", "WorkerLookUp", "WorkerRetrieve",
                        "WorkerRegister", "WorkerSetStatus"):
        """
        worker_obj : Worker object to submit the worker request.
        request_id : Unique requester id.
        """

        worker_response = submit_worker_actions(
            input_json_obj, uri_client, worker_obj, input_method)

        return worker_response
