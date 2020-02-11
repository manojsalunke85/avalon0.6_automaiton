import logging
import json
import time

from src.worker_lookup.worker_lookup_params \
    import WorkerLookUp
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
from src.utilities.verification_utils \
        import validate_response_code
from src.utilities.generic_utils import GetResultWaitTime


logger = logging.getLogger(__name__)


def submit_request(uri_client, input_json_str1, output_json_file_name):
    """ Function to submit request to enclave,
    retrieve response and write files of input and output.
    Input Parameters : uri_client, input_json_str1, output_json_file_name
    Returns : response"""

    req_time = time.strftime("%Y%m%d_%H%M%S")
    input_json_str = json.dumps(input_json_str1)
    # write request to file
    signed_input_file = ('./results/' + output_json_file_name + '_' + req_time
                         + '_request.json')
    with open(signed_input_file, 'w') as req_file:
        req_file.write(json.dumps(input_json_str, ensure_ascii=False))
        # json.dump(input_json_str1, req_file)

    logger.info('**********Received Request*********\n%s\n', input_json_str)
    # submit request and retrieve response
    response = uri_client._postmsg(input_json_str)
    logger.info('**********Received Response*********\n%s\n', response)

    # write response to file
    response_output_file = ('./results/' + output_json_file_name + '_'
                            + req_time + '_response.json')
    with open(response_output_file, 'w') as resp_file:
        resp_file.write(json.dumps(response, ensure_ascii=False))

    return response


def submit_worker_actions(input_request, uri_client, worker_obj,
                          request_method):
    ''' Function to submit worker actions.
        Reads input json file of the test case.
        Triggers create worker request, submit request and validate response.
        Input Parameters : request, id_gen, output_json_file_name,
        worker_obj, uri_client, check_worker_result
        Returns : err_cd, worker_obj, input_json_str1, response. '''

    logger.info("----- Testing Worker Actions -----")

    if constants.worker_request_mode == "object":
        # submit work order get result and retrieve response
        logger.info("----- Constructing Request from input object -----")

        input_action = json.loads(action_obj.to_string())
    else:
        logger.info("----- Constructing Request from input json -----")
        if request_method == "WorkerUpdate":
            action_obj = WorkerUpdate()
        elif request_method == "WorkerSetStatus":
            action_obj = WorkerSetStatus()
        elif request_method == "WorkerRegister":
            action_obj = WorkerRegister()
        elif request_method == "WorkerLookUp":
            action_obj = WorkerLookUp()
            tamper = constants.worker_lookup_tamper
            output_file = constants.worker_lookup_output_json_file_name
        elif request_method == "WorkerRetrieve":
            action_obj = WorkerRetrieve()
            tamper = constants.worker_retrieve_tamper
            output_file = constants.worker_retrieve_output_json_file_name
        else:
            logger.info("----- Invalid Request method -----")

        action_obj.add_json_values(input_request, worker_obj, tamper)
        final_json_str = json.loads(action_obj.to_string())

    # submit work order request and retrieve response
    response = submit_request(uri_client, final_json_str, output_file)

    return response


def submit_work_order_get_result(uri_client,
                                 err_cd, work_order_id,
                                 request_id):
    """ Function to submit work order get result request.
    Uses WorkOrderGetResult class to initialize request object.
    Return err_cd, response."""

    logger.info("------ Testing WorkOrderGetResult ------")

    submiting_time = ""

    if err_cd == 0:
        if constants.wo_result_request_mode == "object":
            # submit work order get result and retrieve response
            logger.info("----- Constructing WorkOrderGetResult -----")
            request_obj = WorkOrderGetResult()
            request_obj.set_work_order_id(work_order_id)
            request_obj.set_request_id(request_id)
            input_get_result = json.loads(request_obj.to_string())
        else:
            request_obj = WorkOrderGetResult()
            request_obj.set_work_order_id(work_order_id)
            request_obj.set_request_id(request_id)
            input_get_result = json.loads(request_obj.to_string())

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
            response = submit_request(
                uri_client, input_get_result,
                constants.wo_result_output_json_file_name)
            time.sleep(GetResultWaitTime.LOOP_WAIT_TIME.value)

    else:
        logger.info('ERROR: WorkOrderGetResult not performed - \
                    Expected response not received for \
                    WorkOrderSubmit.')

    response_tup = (err_cd, response, submiting_time)
    return response_tup


def submit_work_order(input_request,
                      uri_client, worker_obj,
                      private_key, err_cd):
    """ Function to submit work order
        Read input request from string or object and submit request.
        Uses WorkOrderSubmit class definition to initialize work order object.
        Triggers submit_request, validate_response_code,
        Returns - error code, input_json_str1, response, submiting_time,
        worker_obj, sig_obj, encrypted_session_key. """

    response = {}

    if err_cd == 0:
        # --------------------------------------------------------------------
        logger.info("------ Testing WorkOrderSubmit ------")

        if constants.wo_submit_request_mode == "object":
            input_work_order = json.loads(input_request.to_string())
        else:
            # create work order request
            wo_obj = WorkOrderSubmit()
            wo_obj.add_json_values(input_request, worker_obj, private_key,
                                   constants.wo_submit_tamper)
            input_work_order = wo_obj.compute_signature(
                constants.wo_submit_tamper)
            logger.info('Compute Signature complete \n')

        final_json_str = json.loads(input_work_order)
        response = submit_request(uri_client, final_json_str,
                                  constants.wo_submit_output_json_file_name)
        err_cd = validate_response_code(response)

    else:
        logger.info('ERROR: No Worker Retrieved from system.\
                   Unable to proceed to submit work order.')

    response_tup = (err_cd, response, final_json_str, wo_obj)

    return response_tup
