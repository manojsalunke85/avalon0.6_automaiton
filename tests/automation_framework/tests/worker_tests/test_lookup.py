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
from src.libs import constants
from src.utilities.verification_utils \
    import check_worker_lookup_response, check_worker_retrieve_response, \
    validate_response_code
from src.libs.avalon_test_wrapper \
    import process_input, run_test, read_json
from src.utilities.generic_utils import TestStep
import operator
from src.utilities.submit_request_utility import \
    submit_request, submit_lookup_sdk

logger = logging.getLogger(__name__)


def read_config(request_file):
    raw_input_json = read_json(request_file)
    return raw_input_json


def pre_test(setup_config):
    uri_client = setup_config
    logger.info("****URI Client******\n%s\n", uri_client)
    return uri_client


@pytest.mark.worker
@pytest.mark.worker_lookup
@pytest.mark.test_worker_lookup
@pytest.mark.listener
@pytest.mark.sdk
def test_worker_lookup(setup_config):
    request_file = os.path.join(
        constants.worker_input_file,
        "worker_lookup.json")

    uri_client = pre_test(setup_config)

    output_obj, action_obj = process_input(
        read_config(request_file))

    if constants.direct_test_mode == "listener":
        response = submit_request(
            uri_client, output_obj,
            constants.worker_lookup_output_json_file_name)
    else:
        response = submit_lookup_sdk(
            output_obj, read_config(request_file))

    logger.info("**********Received Response*********\n%s\n", response)

    assert (check_worker_lookup_response(response, operator.gt, 0)
            is TestStep.SUCCESS.value)

    logger.info('\t\t!!! Test completed !!!\n\n')


@pytest.mark.worker
@pytest.mark.worker_lookup
@pytest.mark.test_worker_lookup_workerType_not_unsigned_int
@pytest.mark.listener
def test_worker_lookup_workerType_not_unsigned_int(setup_config):
    request_file = os.path.join(
        constants.worker_input_file,
        "worker_lookup_workerType_not_unsigned_int.json")

    uri_client = pre_test(setup_config)

    output_obj, action_obj = process_input(
        read_config(request_file))

    if constants.direct_test_mode == "listener":
        response = submit_request(
            uri_client, output_obj,
            constants.worker_lookup_output_json_file_name)
    else:
        logger.info("***Test not applicable for SDK Direct mode ****\n")

    logger.info("**********Received Response*********\n%s\n", response)

    assert (check_worker_lookup_response(response, operator.eq, 0)
            is TestStep.SUCCESS.value)

    logger.info('\t\t!!! Test completed !!!\n\n')


@pytest.mark.worker
@pytest.mark.worker_lookup
@pytest.mark.test_worker_lookup_empty_params
@pytest.mark.listener
def test_worker_lookup_empty_params(setup_config):
    request_file = os.path.join(
        constants.worker_input_file,
        "worker_lookup_empty_params.json")

    uri_client = pre_test(setup_config)

    output_obj, action_obj = process_input(
        read_config(request_file))

    if constants.direct_test_mode == "listener":
        response = submit_request(
            uri_client, output_obj,
            constants.worker_lookup_output_json_file_name)
    else:
        logger.info("***Test not applicable for SDK Direct mode ****\n")

    logger.info("**********Received Response*********\n%s\n", response)

    assert (check_worker_lookup_response(response, operator.gt, 0)
            is TestStep.SUCCESS.value)

    logger.info('\t\t!!! Test completed !!!\n\n')


@pytest.mark.worker
@pytest.mark.worker_lookup
@pytest.mark.test_worker_lookup_jsonrpc_different_version
@pytest.mark.listener
@pytest.mark.sdk
def test_worker_lookup_jsonrpc_different_version(setup_config):
    request_file = os.path.join(
        constants.worker_input_file,
        "worker_lookup_jsonrpc_different_version.json")

    uri_client = pre_test(setup_config)

    output_obj, action_obj = process_input(
        read_config(request_file))

    if constants.direct_test_mode == "listener":
        response = submit_request(
            uri_client, output_obj,
            constants.worker_lookup_output_json_file_name)
    else:
        response = submit_lookup_sdk(
            output_obj, read_config(request_file))

    logger.info("**********Received Response*********\n%s\n", response)

    assert (check_worker_lookup_response(response, operator.gt, 0)
            is TestStep.SUCCESS.value)

    logger.info('\t\t!!! Test completed !!!\n\n')
