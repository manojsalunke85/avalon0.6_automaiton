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
from src.work_order_submit.work_order_submit_params \
    import WorkOrderSubmit
from src.worker_retrieve.worker_retrieve_params \
    import WorkerRetrieve
from src.work_order_get_result.work_order_get_result_params \
    import WorkOrderGetResult
import avalon_client_sdk.worker.worker_details as worker
from src.libs.avalon_test_wrapper \
    import process_input, read_json
from src.utilities.generic_utils import TestStep
from src.utilities.submit_request_utility import \
    submit_request, submit_create_receipt_sdk
import crypto_utils.crypto_utility as crypto_utils
from src.utilities.verification_utils \
    import verify_test, validate_response_code
from src.utilities.generic_utils import GetResultWaitTime
import time

logger = logging.getLogger(__name__)


def read_config(request_file):
    raw_input_json = read_json(request_file)

    return raw_input_json


def pre_cycle(input_json_obj, uri_client):
    if input_json_obj["method"] == "WorkOrderReceiptCreate":
        lookup_obj = WorkerLookUp()
        test_final_json = lookup_obj.configure_data(
            input_json=None, worker_obj=None, pre_test_response=None)

        lookup_response = submit_request(
            uri_client, test_final_json,
            constants.worker_lookup_output_json_file_name)

        logger.info("******Received Response******\n%s\n", lookup_response)
        worker_obj = worker.SGXWorkerDetails()
        retrieve_obj = WorkerRetrieve()
        input_worker_retrieve = retrieve_obj.configure_data(
            input_json=None, worker_obj=None,
            pre_test_response=lookup_response)
        logger.info('*****Worker details Updated with Worker ID***** \
                       \n%s\n', input_worker_retrieve)
        retrieve_response = submit_request(
            uri_client, input_worker_retrieve,
            constants.worker_retrieve_output_json_file_name)
        worker_obj.load_worker(retrieve_response)
        submit_obj = WorkOrderSubmit()
        submit_request_file = os.path.join(
            constants.work_order_input_file,
            "work_order_success.json")
        submit_request_json = read_config(submit_request_file)
        submit_json = submit_obj.configure_data(
            input_json=submit_request_json, worker_obj=worker_obj,
            pre_test_response=None)
        submit_response = submit_request(
            uri_client, submit_json,
            constants.wo_submit_output_json_file_name)
        input_work_order_submit = submit_obj.compute_signature(
            constants.wo_submit_tamper)
        logger.info("******Work Order submitted*****\n%s\n", submit_response)
    else:
        logger.info("Function called for wrong method name")
        exit(1)
    if constants.direct_test_mode == "listener":
        return worker_obj, uri_client, input_work_order_submit
    else:
        return worker_obj, uri_client, submit_json


def post_cycle(final_json, uri_client):
    logger.info("Call getresult")
    work_order_id = final_json["params"]["workOrderId"]
    request_id = final_json["id"] + 1
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


@pytest.mark.work_order_create_receipt
@pytest.mark.test_work_order_create_receipt
@pytest.mark.listener
@pytest.mark.sdk
def test_work_order_create_receipt(setup_config):
    request_file = os.path.join(
        constants.work_order_receipt,
        "work_order_receipt.json")

    worker_obj, uri_client, input_work_order_submit = pre_cycle(
        read_config(request_file), setup_config)

    output_obj, action_obj = process_input(
        read_config(request_file), worker_obj=worker_obj,
        pre_test_response=input_work_order_submit)

    if constants.direct_test_mode == "listener":
        receipt_response = submit_request(
            uri_client, output_obj,
            constants.wo_submit_output_json_file_name)
    else:
        receipt_response = submit_create_receipt_sdk(
            read_config(request_file), output_obj)
    logger.info("******Receipt response*****\n%s\n", receipt_response)

    assert (validate_response_code(receipt_response)
            is TestStep.SUCCESS.value)
    logger.info('\t\t!!! Test completed !!!\n\n')


@pytest.mark.work_order_create_receipt
@pytest.mark.test_create_work_order_receipt_invalid_requester_id
@pytest.mark.listener
@pytest.mark.sdk
def test_create_work_order_receipt_invalid_requester_id(setup_config):
    request_file = os.path.join(
        constants.work_order_receipt,
        "work_order_receipt_invalid_requester_id.json")

    worker_obj, uri_client, input_work_order_submit = pre_cycle(
        read_config(request_file), setup_config)

    output_obj, action_obj = process_input(
        read_config(request_file), worker_obj=worker_obj,
        pre_test_response=input_work_order_submit)

    if constants.direct_test_mode == "listener":
        receipt_response = submit_request(
            uri_client, output_obj,
            constants.wo_submit_output_json_file_name)
    else:
        receipt_response = submit_create_receipt_sdk(
            read_config(request_file), output_obj)
    logger.info("******Receipt response*****\n%s\n", receipt_response)

    assert (validate_response_code(receipt_response)
            is TestStep.SUCCESS.value)
    logger.info('\t\t!!! Test completed !!!\n\n')


@pytest.mark.work_order_create_receipt
@pytest.mark.test_create_work_order_receipt_hexstr_workorderRequesthash
@pytest.mark.listener
@pytest.mark.sdk
def test_create_work_order_receipt_hexstr_workorderRequesthash(setup_config):
    request_file = os.path.join(
        constants.work_order_receipt,
        "work_order_receipt_hexstr_workorderRequesthash.json")

    worker_obj, uri_client, input_work_order_submit = pre_cycle(
        read_config(request_file), setup_config)

    output_obj, action_obj = process_input(
        read_config(request_file), worker_obj=worker_obj,
        pre_test_response=input_work_order_submit)

    if constants.direct_test_mode == "listener":
        receipt_response = submit_request(
            uri_client, output_obj,
            constants.wo_submit_output_json_file_name)
    else:
        receipt_response = submit_create_receipt_sdk(
            read_config(request_file), output_obj)
    logger.info("******Receipt response*****\n%s\n", receipt_response)

    assert (validate_response_code(receipt_response)
            is TestStep.SUCCESS.value)
    logger.info('\t\t!!! Test completed !!!\n\n')


@pytest.mark.work_order_create_receipt
@pytest.mark.test_create_work_order_receipt_wrong_rverificationkey
@pytest.mark.listener
@pytest.mark.sdk
def test_create_work_order_receipt_wrong_rverificationkey(setup_config):
    request_file = os.path.join(
        constants.work_order_receipt,
        "work_order_receipt_wrong_rverificationkey.json")

    worker_obj, uri_client, input_work_order_submit = pre_cycle(
        read_config(request_file), setup_config)

    output_obj, action_obj = process_input(
        read_config(request_file), worker_obj=worker_obj,
        pre_test_response=input_work_order_submit)

    if constants.direct_test_mode == "listener":
        receipt_response = submit_request(
            uri_client, output_obj,
            constants.wo_submit_output_json_file_name)
    else:
        receipt_response = submit_create_receipt_sdk(
            read_config(request_file), output_obj)
    logger.info("******Receipt response*****\n%s\n", receipt_response)

    assert (validate_response_code(receipt_response)
            is TestStep.SUCCESS.value)
    logger.info('\t\t!!! Test completed !!!\n\n')


@pytest.mark.work_order_create_receipt
@pytest.mark.test_create_work_order_receipt_wrong_rverificationkey
def test_create_work_order_receipt_wrong_rverificationkey(setup_config):
    request_file = os.path.join(
        constants.work_order_receipt,
        "work_order_receipt_wrong_rverificationkey.json")

    worker_obj, uri_client, input_work_order_submit = pre_cycle(
        read_config(request_file), setup_config)

    output_obj, action_obj = process_input(
        read_config(request_file), worker_obj=worker_obj,
        pre_test_response=input_work_order_submit)

    if constants.direct_test_mode == "listener":
        receipt_response = submit_request(
            uri_client, output_obj,
            constants.wo_submit_output_json_file_name)
    else:
        receipt_response = submit_create_receipt_sdk(
            read_config(request_file), output_obj)
    logger.info("******Receipt response*****\n%s\n", receipt_response)

    assert (validate_response_code(receipt_response)
            is TestStep.SUCCESS.value)
    logger.info('\t\t!!! Test completed !!!\n\n')
