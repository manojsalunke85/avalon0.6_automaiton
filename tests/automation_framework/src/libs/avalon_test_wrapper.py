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
    submit_request, submit_work_order, \
    submit_worker_actions, submit_work_order_get_result
TCFHOME = os.environ.get("TCF_HOME", "../../")
logger = logging.getLogger(__name__)


def read_json(request_file):
    # Read the method name from JSON file
    with open(request_file, "r") as file:
        input_json = file.read().rstrip('\n')

    input_json_obj = json.loads(input_json)

    return input_json_obj


def process_input(input_json_obj, worker_obj=None, pre_test_response=None):
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
        output_obj = action_obj.configure_data(
            input_json_obj, worker_obj, pre_test_response)
    else:
        output_obj = action_obj.configure_data_sdk(
            input_json_obj, worker_obj, pre_test_response)

    return output_obj, action_obj
