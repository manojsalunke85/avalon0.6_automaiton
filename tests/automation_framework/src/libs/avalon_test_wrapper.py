import json
import logging
import os
from src.worker_lookup.worker_lookup_params \
    import WorkerLookUp
from src.work_order_receipt.work_order_receipt_params \
    import WorkOrderReceipt
from src.libs import constants
from src.worker_retrieve.worker_retrieve_params \
    import WorkerRetrieve
from src.worker_register.worker_register_params \
    import WorkerRegister
from src.worker_set_status.worker_set_status_params \
    import WorkerSetStatus
from src.worker_update.worker_update_params \
    import WorkerUpdate
from src.work_order_get_result.work_order_get_result_params \
    import WorkOrderGetResult
from src.work_order_submit.work_order_submit_params \
    import WorkOrderSubmit
from src.utilities.submit_request_utility import \
    submit_request_listener, submit_lookup_sdk, \
    submit_retrieve_sdk, submit_create_receipt_sdk, \
    submit_work_order_sdk
import avalon_client_sdk.worker.worker_details as worker
TCFHOME = os.environ.get("TCF_HOME", "../../")
logger = logging.getLogger(__name__)


def read_json(request_file):
    # Read the method name from JSON file
    with open(request_file, "r") as file:
        input_json = file.read().rstrip('\n')

    input_json_obj = json.loads(input_json)

    return input_json_obj


def build_request_obj(input_json_obj,
                      pre_test_output=None, pre_test_response=None):
    request_method = input_json_obj["method"]
    if request_method == "WorkerUpdate":
        action_obj = WorkerUpdate()
    elif request_method == "WorkerSetStatus":
        action_obj = WorkerSetStatus()
    elif request_method == "WorkerRegister":
        action_obj = WorkerRegister()
    elif request_method == "WorkerLookUp":
        action_obj = WorkerLookUp()
    elif request_method == "WorkerRetrieve":
        action_obj = WorkerRetrieve()
    elif request_method == "WorkOrderSubmit":
        action_obj = WorkOrderSubmit()
    elif request_method == "WorkOrderGetResult":
        action_obj = WorkOrderGetResult()
    elif request_method == "WorkOrderReceiptCreate":
        action_obj = WorkOrderReceipt()
    if constants.direct_test_mode == "listener":
        request_obj = action_obj.configure_data(
            input_json_obj, pre_test_output, pre_test_response)
    else:
        request_obj = action_obj.configure_data_sdk(
            input_json_obj, pre_test_output, pre_test_response)

    return request_obj, action_obj


def submit_request(uri_client, output_obj, output_file, input_file):
    request_method = input_file["method"]
    if constants.direct_test_mode == "listener":
        submit_response = submit_request_listener(
            uri_client, output_obj, output_file)
    else:
        if request_method == "WorkerLookUp":
            submit_response = submit_lookup_sdk(
                output_obj, input_file)
        elif request_method == "WorkerRetrieve":
            submit_response = submit_retrieve_sdk(
                output_obj, input_file)
        elif request_method == "WorkOrderSubmit":
            submit_response = submit_work_order_sdk(
                output_obj, input_file)
        elif request_method == "WorkOrderReceiptCreate":
            submit_response = submit_create_receipt_sdk(
                output_obj, input_file)
    return submit_response


def worker_lookup(uri_client):
    lookup_obj = WorkerLookUp()
    test_final_json = lookup_obj.configure_data(
        input_json=None, worker_obj=None, pre_test_response=None)

    lookup_response = submit_request_listener(
        uri_client, test_final_json,
        constants.worker_lookup_output_json_file_name)
    return lookup_response


def worker_retrieve(uri_client, lookup_response):
    worker_obj = worker.SGXWorkerDetails()
    retrieve_obj = WorkerRetrieve()
    input_worker_retrieve = retrieve_obj.configure_data(
        input_json=None, worker_obj=None,
        pre_test_response=lookup_response)
    logger.info('*****Worker details Updated with Worker ID***** \
                                   \n%s\n', input_worker_retrieve)
    retrieve_response = submit_request_listener(
        uri_client, input_worker_retrieve,
        constants.worker_retrieve_output_json_file_name)
    worker_obj.load_worker(retrieve_response)

    return worker_obj


def work_order_submit(uri_client, worker_obj):
    submit_obj = WorkOrderSubmit()
    submit_request_file = os.path.join(
        constants.work_order_input_file,
        "work_order_success.json")
    submit_request_json = read_json(submit_request_file)
    submit_json = submit_obj.configure_data(
        input_json=submit_request_json, worker_obj=worker_obj,
        pre_test_response=None)
    submit_response = submit_request_listener(
        uri_client, submit_json,
        constants.wo_submit_output_json_file_name)
    input_work_order_submit = submit_obj.compute_signature(
        constants.wo_submit_tamper)
    logger.info("******Work Order submitted*****\n%s\n", submit_response)
    if constants.direct_test_mode == "listener":
        return input_work_order_submit
    else:
        return submit_json


def pre_test_env(input_file, uri_client):
    request_method = input_file["method"]

    if request_method == "WorkerRetrieve":

        lookup_response = worker_lookup(uri_client)
        logger.info("******Received Response******\n%s\n", lookup_response)
        return lookup_response

    if request_method == "WorkOrderSubmit":
        lookup_response = worker_lookup(uri_client)
        worker_obj = worker_retrieve(uri_client, lookup_response)
        return worker_obj

    if request_method == "WorkOrderReceiptCreate":
        lookup_response = worker_lookup(uri_client)
        worker_obj = worker_retrieve(uri_client, lookup_response)
        wo_submit = work_order_submit(uri_client, worker_obj)
        return worker_obj, wo_submit

    if request_method == "WorkerUpdate" or \
            request_method == "WorkerSetStatus" or \
            request_method == "WorkerRegister":
        logger.info("No setup required for \n%s\n", request_method)
        return 0
