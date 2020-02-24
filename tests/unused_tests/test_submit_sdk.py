# Copyright 2019 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
import logging
import os
import json
from src.libs import constants
from src.worker_lookup.worker_lookup_params \
    import WorkerLookUp
from src.worker_retrieve.worker_retrieve_params \
    import WorkerRetrieve
from src.work_order_get_result.work_order_get_result_params \
    import WorkOrderGetResult
import avalon_client_sdk.worker.worker_details as worker
from src.libs.avalon_test_wrapper \
    import process_and_update, run_test, read_json
from src.utilities.generic_utils import TestStep
from src.utilities.submit_request_utility import \
    submit_request, submit_request_sdk
from src.utilities.verification_utils \
    import verify_test, validate_response_code
from src.utilities.generic_utils import GetResultWaitTime
import time
logger = logging.getLogger(__name__)


def read_config(request_file):
    raw_input_json = read_json(request_file)

    return raw_input_json


def pre_cycle(input_json_obj, uri_client):
    if input_json_obj["method"] == "WorkOrderSubmit":
        lookup_obj = WorkerLookUp()
        test_final_json = lookup_obj.configure_data(
            input_json=None, worker_obj=None, lookup_response=None)

        lookup_response = submit_request(
            uri_client, test_final_json,
            constants.worker_lookup_output_json_file_name)

        logger.info("******Received Response******\n%s\n", lookup_response)
        worker_obj = worker.SGXWorkerDetails()
        retrieve_obj = WorkerRetrieve()
        input_worker_retrieve = retrieve_obj.configure_data(
            input_json=None, worker_obj=None, lookup_response=lookup_response)
        logger.info('*****Worker details Updated with Worker ID***** \
                       \n%s\n', input_worker_retrieve)
        retrieve_response = submit_request(
            uri_client, input_worker_retrieve,
            constants.worker_retrieve_output_json_file_name)
        worker_obj.load_worker(retrieve_response)
    else:
        logger.info("Function called for wrong method name")
        exit(1)
    return worker_obj, uri_client


def post_cycle(final_json, uri_client):
    logger.info("Call getresult")
    if constants.direct_test_mode == "listener":
        work_order_id = final_json["params"]["workOrderId"]
        request_id = final_json["id"] + 1
    else:
        request_id = 12
        work_order_id = final_json.get_work_order_id()
    logger.info("Requester ID is %s\n", request_id)
    logger.info("Work order ID is %s\n", work_order_id)
    getresult_obj = WorkOrderGetResult()
    getresult_json = getresult_obj.configure_data(request_id, work_order_id)
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
            uri_client, getresult_json,
            constants.wo_result_output_json_file_name)
        time.sleep(GetResultWaitTime.LOOP_WAIT_TIME.value)
        logger.info("******Received Response*****\n%s\n", response)
    return response


@pytest.mark.work_order
@pytest.mark.work_order_success
def test_work_order_success(setup_config):
    request_file = os.path.join(
        constants.work_order_input_file,
        "work_order_success.json")

    worker_obj, uri_client = pre_cycle(
        read_config(request_file), setup_config)

    test_final_json, work_order_obj = process_and_update(
        read_config(request_file), worker_obj=worker_obj)

    submit_response = submit_request_sdk(
        read_config(request_file), test_final_json)

    result_response = post_cycle(test_final_json, uri_client)

    assert (
            verify_test(result_response, worker_obj, work_order_obj)
            is TestStep.SUCCESS.value)
    logger.info('\t\t!!! Test completed !!!\n\n')
