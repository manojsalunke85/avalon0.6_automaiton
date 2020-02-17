import json
import logging
from src.libs import constants
import crypto_utils.crypto_utility as enclave_helper

from src.utilities.submit_request_utility import \
    submit_request, submit_work_order, \
    submit_worker_actions, submit_work_order_get_result

from src.libs.direct_client_sdk import \
    submit_work_order_client_sdk, get_work_order_result_sdk, \
    worker_lookup_sdk, get_worker_id_sdk, worker_retrieve_details_sdk, \
    worker_initialize_sdk

from src.libs.listener import \
    worker_lookup_listener, worker_retrieve_listener, \
    work_setstatus_listener
logger = logging.getLogger(__name__)


def read_json(request_file):
    # Read the method name from JSON file
    with open(request_file, "r") as file:
        input_json = file.read().rstrip('\n')

    input_json_obj = json.loads(input_json)

    return input_json_obj


def run_test(input_json_obj, setup_config):

    input_method = input_json_obj["method"]

    # private_key of client
    private_key = enclave_helper.generate_signing_keys()

    if constants.direct_test_mode == "listener":

        if input_method == "WorkOrderSubmit":
            """
            worker_obj :  Worker object to submit the work order request.
            private_key : Private key used to submit the request.
            err_cd : Status of previous request (worker retrieve)
            Success or Fail.
            """
            uri_client, worker_obj, err_cd, retrieve_response = setup_config

            (err_cd, work_order_submit_response,
             final_json_str, work_order_obj) = submit_work_order(
                input_json_obj, uri_client,
                worker_obj, private_key, err_cd)

            work_order_id = final_json_str["params"]["workOrderId"]
            request_id = final_json_str["id"] + 1

            err_cd, work_order_get_result_response, submiting_time = \
                submit_work_order_get_result(
                    uri_client, err_cd, work_order_id, request_id)

            return \
                work_order_submit_response, \
                work_order_get_result_response, worker_obj, work_order_obj

        elif input_method == "WorkOrderGetResult":
            """
            err_cd : Status of previous request (work order submit).
            work_order_id : Same work order id as in work order submit.
            request_id : Unique requester id.

            err_cd, work_order_id, request_id = request_tup[6:9]

            response_tup = submit_work_order_get_result(
                input_request, request_mode, tamper, output_json_file_name,
                uri_client, err_cd, work_order_id, request_id)"""

            logger.info("Code for get result flow\n")

        elif input_method == "WorkerLookUp":
            """
            worker_obj : Worker object to submit the worker request.
            request_id : Unique requester id.
            """

            logger.info("Inside WorkerLookup for Listener\n")
            uri_client = setup_config
            worker_response = worker_lookup_listener(
                uri_client, input_json_obj)

            return worker_response

        elif input_method == "WorkerRetrieve":
            logger.info("Inside WorkerRetrieve for Listener\n")
            uri_client = setup_config
            worker_response = worker_lookup_listener(uri_client)

            worker_obj, err_cd, worker_response = \
                worker_retrieve_listener(
                    worker_response, uri_client, input_json_obj)

            return worker_response

        elif input_method == "WorkerSetStatus":
            logger.info("Inside WorkerSetStatus for Listener\n")
            uri_client = setup_config
            worker_response = worker_lookup_listener(uri_client)

            worker_obj, err_cd, worker_retrieve_response = \
                worker_retrieve_listener(
                    worker_response, uri_client, input_json_obj)

            worker_response = work_setstatus_listener(
                worker_obj, uri_client, input_json_obj)

            return worker_response

    else:

        jrpc_req_id = 31

        if input_method == "WorkOrderSubmit":

            # Create work order using client SDK

            worker_lookup_response, worker_registry = worker_lookup_sdk(
                jrpc_req_id)

            worker_id = get_worker_id_sdk(worker_lookup_response)

            worker_retrieve_response = worker_retrieve_details_sdk(
                worker_registry, jrpc_req_id, worker_id)

            worker_obj = worker_initialize_sdk(
                worker_retrieve_response, worker_id)

            work_order_submit_response, work_order_obj, wo_params = \
                submit_work_order_client_sdk(
                    input_json_obj, worker_obj)

            get_result_id = input_json_obj["id"] + 1

            work_order_get_result_response = \
                get_work_order_result_sdk(
                    work_order_obj, wo_params, get_result_id)

            logger.info("Test over using SDK\n")

            return \
                work_order_submit_response, \
                work_order_get_result_response, worker_obj, wo_params

        elif input_method == "WorkerLookUp":
            logger.info("Inside WorkerLookup for SDK\n")
            worker_lookup_response, worker_registry = worker_lookup_sdk(
                jrpc_req_id, input_json=input_json_obj)

            return worker_lookup_response

        elif input_method == "WorkerRetrieve":
            logger.info("Inside WorkerRetrieve for SDK\n")
            worker_lookup_response, worker_registry = worker_lookup_sdk(
                jrpc_req_id)

            worker_id = get_worker_id_sdk(worker_lookup_response)

            worker_retrieve_response = worker_retrieve_details_sdk(
                worker_registry, jrpc_req_id, worker_id)

            return worker_retrieve_response
