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
    import process_input, run_test, read_json
from src.utilities.generic_utils import TestStep
from src.utilities.submit_request_utility import \
    submit_request, submit_request_sdk
import crypto_utils.crypto_utility as crypto_utils
from src.utilities.verification_utils \
    import verify_test, validate_response_code
from src.utilities.generic_utils import GetResultWaitTime
import time
logger = logging.getLogger(__name__)


def read_config(request_file):
    raw_input_json = read_json(request_file)

    return raw_input_json


def pre_test(input_json_obj, uri_client):
    if input_json_obj["method"] == "WorkOrderSubmit":
        lookup_obj = WorkerLookUp()
        output_obj_lookup = lookup_obj.configure_data(
            input_json=None, worker_obj=None, pre_test_response=None)

        lookup_response = submit_request(
            uri_client, output_obj_lookup,
            constants.worker_lookup_output_json_file_name)

        logger.info("******Received Response******\n%s\n", lookup_response)
        worker_obj = worker.SGXWorkerDetails()
        retrieve_obj = WorkerRetrieve()
        output_obj_retrieve = retrieve_obj.configure_data(
            input_json=None, worker_obj=None,
            pre_test_response=lookup_response)
        logger.info('*****Worker details Updated with Worker ID***** \
                       \n%s\n', output_obj_retrieve)
        retrieve_response = submit_request(
            uri_client, output_obj_retrieve,
            constants.worker_retrieve_output_json_file_name)
        worker_obj.load_worker(retrieve_response)
    else:
        logger.info("Function called for wrong method name")
        exit(1)
    return worker_obj, uri_client


def post_test(output_obj, uri_client):
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
        response = submit_request(
            uri_client, output_obj_getresult,
            constants.wo_result_output_json_file_name)
        time.sleep(GetResultWaitTime.LOOP_WAIT_TIME.value)
        logger.info("******Received Response*****\n%s\n", response)
    return response


@pytest.mark.work_order_submit
@pytest.mark.test_work_order_success
@pytest.mark.listener
@pytest.mark.sdk
def test_work_order_success(setup_config):
    request_file = os.path.join(
        constants.work_order_input_file,
        "work_order_success.json")

    worker_obj, uri_client = pre_test(
        read_config(request_file), setup_config)

    output_obj, action_obj = process_input(
        read_config(request_file), worker_obj=worker_obj)

    if constants.direct_test_mode == "listener":
        submit_response = submit_request(
            uri_client, output_obj,
            constants.wo_submit_output_json_file_name)
    else:
        submit_response = submit_request_sdk(
            read_config(request_file), output_obj)

    result_response = post_test(output_obj, uri_client)

    assert (
        verify_test(result_response, worker_obj, action_obj)
        is TestStep.SUCCESS.value)
    logger.info('\t\t!!! Test completed !!!\n\n')


@pytest.mark.work_order_submit
@pytest.mark.test_work_order_inData_DataEncryptionKey_hyphen_echo
@pytest.mark.listener
@pytest.mark.sdk
def test_work_order_inData_DataEncryptionKey_hyphen_echo(setup_config):
    request_file = os.path.join(
        constants.work_order_input_file,
        "work_order_inData_DataEncryptionKey_hyphen_echo.json")

    worker_obj, uri_client = pre_test(
        read_config(request_file), setup_config)

    output_obj, action_obj = process_input(
        read_config(request_file), worker_obj=worker_obj)

    if constants.direct_test_mode == "listener":
        submit_response = submit_request(
            uri_client, output_obj,
            constants.wo_submit_output_json_file_name)
    else:
        submit_response = submit_request_sdk(
            read_config(request_file), output_obj)

    result_response = post_test(output_obj, uri_client)

    assert (validate_response_code(result_response)
            is TestStep.SUCCESS.value)
    logger.info('\t\t!!! Test completed !!!\n\n')


@pytest.mark.work_order_submit
@pytest.mark.test_work_order_data_datahash_null
@pytest.mark.listener
@pytest.mark.sdk
def test_work_order_data_datahash_null(setup_config):
    request_file = os.path.join(
        constants.work_order_input_file,
        "work_order_data_datahash_null.json")

    worker_obj, uri_client = pre_test(
        read_config(request_file), setup_config)

    output_obj, action_obj = process_input(
        read_config(request_file), worker_obj=worker_obj)

    if constants.direct_test_mode == "listener":
        submit_response = submit_request(
            uri_client, output_obj,
            constants.wo_submit_output_json_file_name)
    else:
        submit_response = submit_request_sdk(
            read_config(request_file), output_obj)

    result_response = post_test(output_obj, uri_client)

    assert (
        verify_test(result_response, worker_obj, action_obj)
        is TestStep.SUCCESS.value)
    logger.info('\t\t!!! Test completed !!!\n\n')


@pytest.mark.work_order_submit
@pytest.mark.test_work_order_submit_requesterId_null
@pytest.mark.listener
@pytest.mark.sdk
def test_work_order_submit_requesterId_null(setup_config):
    request_file = os.path.join(
        constants.work_order_input_file,
        "work_order_requester_id_null.json")

    worker_obj, uri_client = pre_test(
        read_config(request_file), setup_config)

    output_obj, action_obj = process_input(
        read_config(request_file), worker_obj=worker_obj)

    if constants.direct_test_mode == "listener":
        submit_response = submit_request(
            uri_client, output_obj,
            constants.wo_submit_output_json_file_name)
    else:
        submit_response = submit_request_sdk(
            read_config(request_file), output_obj)

    result_response = post_test(output_obj, uri_client)

    assert (
        verify_test(result_response, worker_obj, action_obj)
        is TestStep.SUCCESS.value)
    logger.info('\t\t!!! Test completed !!!\n\n')


@pytest.mark.work_order_submit
@pytest.mark.test_work_order_submit_sessionkeyiv_and_iv_indata_hex_string
@pytest.mark.listener
@pytest.mark.sdk
def test_work_order_submit_sessionkeyiv_and_iv_indata_hex_string(
        setup_config):
    request_file = os.path.join(
        constants.work_order_input_file,
        "work_order_iv_indata_hex_string.json")

    worker_obj, uri_client = pre_test(
        read_config(request_file), setup_config)

    output_obj, action_obj = process_input(
        read_config(request_file), worker_obj=worker_obj)

    if constants.direct_test_mode == "listener":
        submit_response = submit_request(
            uri_client, output_obj,
            constants.wo_submit_output_json_file_name)
    else:
        submit_response = submit_request_sdk(
            read_config(request_file), output_obj)

    result_response = post_test(output_obj, uri_client)

    assert (
        verify_test(result_response, worker_obj, action_obj)
        is TestStep.SUCCESS.value)
    logger.info('\t\t!!! Test completed !!!\n\n')


@pytest.mark.work_order_submit
@pytest.mark.test_work_order_get_result
@pytest.mark.listener
@pytest.mark.sdk
def test_work_order_get_result(setup_config):
    request_file = os.path.join(
        constants.work_order_input_file,
        "work_order_get_result.json")

    worker_obj, uri_client = pre_test(
        read_config(request_file), setup_config)

    output_obj, action_obj = process_input(
        read_config(request_file), worker_obj=worker_obj)

    if constants.direct_test_mode == "listener":
        submit_response = submit_request(
            uri_client, output_obj,
            constants.wo_submit_output_json_file_name)
    else:
        submit_response = submit_request_sdk(
            read_config(request_file), output_obj)

    result_response = post_test(output_obj, uri_client)

    assert (
        verify_test(result_response, worker_obj, action_obj)
        is TestStep.SUCCESS.value)
    logger.info('\t\t!!! Test completed !!!\n\n')


@pytest.mark.work_order_submit
@pytest.mark.test_work_order_verify_signature
@pytest.mark.listener
@pytest.mark.sdk
def test_work_order_verify_signature(setup_config):
    request_file = os.path.join(
        constants.work_order_input_file,
        "work_order_verify_signature.json")

    worker_obj, uri_client = pre_test(
        read_config(request_file), setup_config)

    output_obj, action_obj = process_input(
        read_config(request_file), worker_obj=worker_obj)

    if constants.direct_test_mode == "listener":
        submit_response = submit_request(
            uri_client, output_obj,
            constants.wo_submit_output_json_file_name)
    else:
        submit_response = submit_request_sdk(
            read_config(request_file), output_obj)

    result_response = post_test(output_obj, uri_client)

    assert (
        verify_test(result_response, worker_obj, action_obj)
        is TestStep.SUCCESS.value)
    logger.info('\t\t!!! Test completed !!!\n\n')


@pytest.mark.work_order_submit
@pytest.mark.test_work_order_submit_requesterNonce_all_special_characters
@pytest.mark.listener
@pytest.mark.sdk
def test_work_order_submit_requesterNonce_all_special_characters(setup_config):
    request_file = os.path.join(
        constants.work_order_input_file,
        "work_order_submit_requesterNonce_all_special_characters.json")

    worker_obj, uri_client = pre_test(
        read_config(request_file), setup_config)

    output_obj, action_obj = process_input(
        read_config(request_file), worker_obj=worker_obj)

    if constants.direct_test_mode == "listener":
        submit_response = submit_request(
            uri_client, output_obj,
            constants.wo_submit_output_json_file_name)
    else:
        submit_response = submit_request_sdk(
            read_config(request_file), output_obj)

    result_response = post_test(output_obj, uri_client)

    assert (
        verify_test(result_response, worker_obj, action_obj)
        is TestStep.SUCCESS.value)
    logger.info('\t\t!!! Test completed !!!\n\n')


@pytest.mark.work_order_submit
@pytest.mark.test_work_order_workerEncryptionKey_special_character
@pytest.mark.listener
@pytest.mark.sdk
def test_work_order_workerEncryptionKey_special_character(setup_config):
    request_file = os.path.join(
        constants.work_order_input_file,
        "work_order_workerEncryptionKey_special_character.json")

    worker_obj, uri_client = pre_test(
        read_config(request_file), setup_config)

    output_obj, action_obj = process_input(
        read_config(request_file), worker_obj=worker_obj)

    if constants.direct_test_mode == "listener":
        submit_response = submit_request(
            uri_client, output_obj,
            constants.wo_submit_output_json_file_name)
    else:
        submit_response = submit_request_sdk(
            read_config(request_file), output_obj)

    result_response = post_test(output_obj, uri_client)

    assert (
        verify_test(result_response, worker_obj, action_obj)
        is TestStep.SUCCESS.value)
    logger.info('\t\t!!! Test completed !!!\n\n')


@pytest.mark.work_order_submit
@pytest.mark.test_work_order_with_alternate_worker_signing_algorithm
@pytest.mark.listener
@pytest.mark.sdk
def test_work_order_with_alternate_worker_signing_algorithm(setup_config):
    request_file = os.path.join(
        constants.work_order_input_file,
        "test_work_order_with_alternate_worker_signing_algorithm.json")

    worker_obj, uri_client = pre_test(
        read_config(request_file), setup_config)

    output_obj, action_obj = process_input(
        read_config(request_file), worker_obj=worker_obj)

    if constants.direct_test_mode == "listener":
        submit_response = submit_request(
            uri_client, output_obj,
            constants.wo_submit_output_json_file_name)
    else:
        submit_response = submit_request_sdk(
            read_config(request_file), output_obj)

    result_response = post_test(output_obj, uri_client)

    assert (
        verify_test(result_response, worker_obj, action_obj)
        is TestStep.SUCCESS.value)
    logger.info('\t\t!!! Test completed !!!\n\n')


@pytest.mark.work_order_submit
@pytest.mark.test_work_order_with_alternate_worker_signing_algorithm
@pytest.mark.listener
@pytest.mark.sdk
def test_work_order_with_alternate_worker_signing_algorithm(setup_config):
    request_file = os.path.join(
        constants.work_order_input_file,
        "work_order_with_alternate_worker_signing_algorithm.json")

    worker_obj, uri_client = pre_test(
        read_config(request_file), setup_config)

    output_obj, action_obj = process_input(
        read_config(request_file), worker_obj=worker_obj)

    if constants.direct_test_mode == "listener":
        submit_response = submit_request(
            uri_client, output_obj,
            constants.wo_submit_output_json_file_name)
    else:
        submit_response = submit_request_sdk(
            read_config(request_file), output_obj)

    result_response = post_test(output_obj, uri_client)

    worker_obj.signingAlgorithm = "RSA-OAEP-3072"

    assert (
        verify_test(result_response, worker_obj, action_obj)
        is TestStep.SUCCESS.value)
    logger.info('\t\t!!! Test completed !!!\n\n')


@pytest.mark.work_order_submit
@pytest.mark.test_work_order_with_alternate_hashing_algorithm
@pytest.mark.listener
@pytest.mark.sdk
def test_work_order_with_alternate_hashing_algorithm(setup_config):
    request_file = os.path.join(
        constants.work_order_input_file,
        "work_order_with_alternate_hashing_algorithm.json")

    worker_obj, uri_client = pre_test(
        read_config(request_file), setup_config)

    output_obj, action_obj = process_input(
        read_config(request_file), worker_obj=worker_obj)

    if constants.direct_test_mode == "listener":
        submit_response = submit_request(
            uri_client, output_obj,
            constants.wo_submit_output_json_file_name)
    else:
        submit_response = submit_request_sdk(
            read_config(request_file), output_obj)

    result_response = post_test(output_obj, uri_client)

    assert (
        verify_test(result_response, worker_obj, action_obj)
        is TestStep.SUCCESS.value)
    logger.info('\t\t!!! Test completed !!!\n\n')


@pytest.mark.work_order_submit
@pytest.mark.test_work_order_without_requester_private_key
@pytest.mark.listener
@pytest.mark.sdk
def test_work_order_without_requester_private_key(setup_config):
    request_file = os.path.join(
        constants.work_order_input_file,
        "work_order_without_requester_private_key.json")

    worker_obj, uri_client = pre_test(
        read_config(request_file), setup_config)

    output_obj, action_obj = process_input(
        read_config(request_file), worker_obj=worker_obj)

    if constants.direct_test_mode == "listener":
        submit_response = submit_request(
            uri_client, output_obj,
            constants.wo_submit_output_json_file_name)
    else:
        submit_response = submit_request_sdk(
            read_config(request_file), output_obj)

    result_response = post_test(output_obj, uri_client)

    assert (
        verify_test(result_response, worker_obj, action_obj)
        is TestStep.SUCCESS.value)
    logger.info('\t\t!!! Test completed !!!\n\n')


@pytest.mark.work_order_submit
@pytest.mark.test_work_order_submit_twice_params
@pytest.mark.listener
@pytest.mark.sdk
def test_work_order_submit_twice_params(setup_config):
    request_file = os.path.join(
        constants.work_order_input_file,
        "work_order_submit_twice_params.json")

    worker_obj, uri_client = pre_test(
        read_config(request_file), setup_config)

    output_obj, action_obj = process_input(
        read_config(request_file), worker_obj=worker_obj)

    if constants.direct_test_mode == "listener":
        submit_response = submit_request(
            uri_client, output_obj,
            constants.wo_submit_output_json_file_name)
    else:
        submit_response = submit_request_sdk(
            read_config(request_file), output_obj)

    result_response = post_test(output_obj, uri_client)

    assert (
        verify_test(result_response, worker_obj, action_obj)
        is TestStep.SUCCESS.value)
    logger.info('\t\t!!! Test completed !!!\n\n')


@pytest.mark.work_order_submit
@pytest.mark.test_work_order_invalid_parameter
@pytest.mark.listener
@pytest.mark.sdk
def test_work_order_invalid_parameter(setup_config):
    request_file = os.path.join(
        constants.work_order_input_file,
        "work_order_invalid_parameter.json")

    worker_obj, uri_client = pre_test(
        read_config(request_file), setup_config)

    output_obj, action_obj = process_input(
        read_config(request_file), worker_obj=worker_obj)

    if constants.direct_test_mode == "listener":
        submit_response = submit_request(
            uri_client, output_obj,
            constants.wo_submit_output_json_file_name)
    else:
        submit_response = submit_request_sdk(
            read_config(request_file), output_obj)

    result_response = post_test(output_obj, uri_client)

    assert (
        verify_test(result_response, worker_obj, action_obj)
        is TestStep.SUCCESS.value)
    logger.info('\t\t!!! Test completed !!!\n\n')
