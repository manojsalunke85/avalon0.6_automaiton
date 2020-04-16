import json
import logging
import os
from src.worker_lookup.worker_lookup_params \
    import WorkerLookUp
from src.work_order_receipt.work_order_receipt_params \
    import WorkOrderReceipt
from src.work_order_receipt.work_order_receipt_retrieve_params \
    import WorkOrderReceiptRetrieve
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
    submit_work_order_sdk, submit_register_sdk, \
    submit_setstatus_sdk, submit_retrieve_receipt_sdk, \
    submit_update_sdk
from src.libs.direct_listener import ListenerImpl
from src.libs.direct_sdk import SDKImpl
import globals
import avalon_sdk.worker.worker_details as worker
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
    """
    This function is used after the pre_test_env and for the
    actual request method passed in the test JSON file. Depending on the
    test mode and the request method, it will call the corresponding
    configure_data function.

    Output: request obj which is the final JSON object in case of the
    listener mode, for SDK mode it is the parameter required by the SDK
    function of the request method
    action_obj is the object of the request method class.

    For ex:
    worker_lookup SDK function requires worker_type parameter
    worker_retrieve SDK function requires worker_id parameter.
    """
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
    elif request_method == "WorkOrderReceiptRetrieve":
        action_obj = WorkOrderReceiptRetrieve()
    if constants.direct_test_mode == "listener":
        request_obj = action_obj.configure_data(
            input_json_obj, pre_test_output, pre_test_response)
    else:
        request_obj = action_obj.configure_data_sdk(
            input_json_obj, pre_test_output, pre_test_response)

    return request_obj, action_obj


def submit_request(uri_client, output_obj, output_file, input_file):
    """
    Single function that is called from the test with the relevant input parameters.
    For listener, output_obj is the JSON obj, for SDK it is the parameter that is received
    as an output from build_request_obj function.
    """
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
        elif request_method == "WorkOrderReceiptRetrieve":
            submit_response = submit_retrieve_receipt_sdk(
                output_obj, input_file)
        elif request_method == "WorkerRegister":
            submit_response = submit_register_sdk(
                output_obj, input_file)
        elif request_method == "WorkerSetStatus":
            submit_response = submit_setstatus_sdk(
                output_obj, input_file)
        elif request_method == "WorkerUpdate":
            submit_response = submit_update_sdk(
                output_obj, input_file)
    return submit_response



def impl_instance():
    if constants.direct_test_mode == "sdk":
        logger.info("Inside SDK instance\n")
        return SDKImpl()
    elif constants.direct_test_mode == "listener":
        logger.info("Inside Listener instance\n")
        return ListenerImpl()


def pre_test_env(input_file):
    """
    This function sets up the environment required to run the test.
    For ex: Work Order Submit test requires worker_lookup, retrieve
    the worker details and pass that as the output.
    """
    request_method = input_file["method"]
    impl_type = impl_instance()

    if request_method == "WorkerRetrieve" or \
            request_method == "WorkerUpdate":

        lookup_response = impl_type.worker_lookup()
        logger.info("******Received Response******\n%s\n", lookup_response)
        return lookup_response

    if request_method == "WorkOrderSubmit":
        lookup_response = impl_type.worker_lookup()
        worker_obj = impl_type.worker_retrieve(lookup_response)
        return worker_obj

    if request_method == "WorkOrderReceiptCreate":
        lookup_response = impl_type.worker_lookup()
        worker_obj = impl_type.worker_retrieve(lookup_response)
        wo_submit = impl_type.work_order_submit(worker_obj)
        return worker_obj, wo_submit

    if  request_method == "WorkOrderReceiptRetrieve":
        lookup_response = impl_type.worker_lookup()
        worker_obj = impl_type.worker_retrieve(lookup_response)
        wo_submit = impl_type.work_order_submit(worker_obj)
        wo_create_receipt = impl_type.work_order_create_receipt(wo_submit)
        return worker_obj, wo_submit

    if request_method == "WorkerSetStatus" or \
            request_method == "WorkerRegister":
        logger.info("No setup required for \n%s\n", request_method)
        return 0
