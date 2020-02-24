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
from src.worker_lookup.worker_lookup_params \
    import WorkerLookUp
from src.worker_retrieve.worker_retrieve_params \
    import WorkerRetrieve
from src.libs.avalon_test_wrapper \
    import process_input, read_json
from src.utilities.generic_utils import TestStep
import operator
import avalon_client_sdk.worker.worker_details as worker
from src.utilities.submit_request_utility import \
    submit_request, submit_lookup_sdk

logger = logging.getLogger(__name__)


def read_config(request_file):
    raw_input_json = read_json(request_file)
    return raw_input_json


def pre_test(input_json_obj, setup_config):
    uri_client = setup_config
    logger.info("****URI Client******\n%s\n", uri_client)
    if input_json_obj["method"] == "WorkerUpdate":
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
    return worker_obj, uri_client


@pytest.mark.worker
@pytest.mark.test_worker_update
def test_worker_update(setup_config):
    request_file = os.path.join(
        constants.worker_input_file,
        "worker_update.json")

    worker_obj, uri_client = pre_test(
        read_config(request_file), setup_config)

    test_final_json, work_order_obj = process_input(
        read_config(request_file), worker_obj=worker_obj)

    if constants.direct_test_mode == "listener":
        response = submit_request(
            uri_client, test_final_json,
            constants.worker_lookup_output_json_file_name)

    logger.info("**********Received Response*********\n%s\n", response)

    assert (validate_response_code(response)
            is TestStep.SUCCESS.value)

    logger.info('\t\t!!! Test completed !!!\n\n')


@pytest.mark.worker
@pytest.mark.test_worker_update_unknown_parameter
def test_worker_update_unknown_parameter(setup_config):
    request_file = os.path.join(
        constants.worker_input_file,
        "worker_update_unknown_parameter.json")

    worker_obj, uri_client = pre_test(
        read_config(request_file), setup_config)

    test_final_json, work_order_obj = process_input(
        read_config(request_file), worker_obj=worker_obj)

    if constants.direct_test_mode == "listener":
        response = submit_request(
            uri_client, test_final_json,
            constants.worker_lookup_output_json_file_name)

    logger.info("**********Received Response*********\n%s\n", response)

    assert (validate_response_code(response)
            is TestStep.SUCCESS.value)

    logger.info('\t\t!!! Test completed !!!\n\n')


@pytest.mark.worker
@pytest.mark.test_worker_update_invalid_parameter
def test_worker_update_invalid_parameter(setup_config):
    request_file = os.path.join(
        constants.worker_input_file,
        "worker_update_invalid_parameter.json")

    worker_obj, uri_client = pre_test(
        read_config(request_file), setup_config)

    test_final_json, work_order_obj = process_input(
        read_config(request_file), worker_obj=worker_obj)

    if constants.direct_test_mode == "listener":
        response = submit_request(
            uri_client, test_final_json,
            constants.worker_lookup_output_json_file_name)

    logger.info("**********Received Response*********\n%s\n", response)

    assert (validate_response_code(response)
            is TestStep.SUCCESS.value)

    logger.info('\t\t!!! Test completed !!!\n\n')
