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
from src.worker_lookup.worker_lookup_params \
    import WorkerLookUp
from src.utilities.verification_utils \
    import check_worker_lookup_response, check_worker_retrieve_response, \
    validate_response_code
from src.libs.avalon_test_wrapper \
    import process_input, read_json
from src.utilities.generic_utils import TestStep
import operator
from src.utilities.submit_request_utility import \
    submit_request, submit_retrieve_sdk

logger = logging.getLogger(__name__)


def read_config(request_file):
    raw_input_json = read_json(request_file)

    return raw_input_json


def pre_test(input_json_obj, setup_config):
    uri_client = setup_config
    if input_json_obj["method"] == "WorkerRetrieve":
        lookup_obj = WorkerLookUp()
        updated_json = lookup_obj.configure_data(
            input_json=None, worker_obj=None, pre_test_response=None)

        response = submit_request(
            uri_client, updated_json,
            constants.worker_lookup_output_json_file_name)

        logger.info("**********Received Response*********\n%s\n", response)

    else:
        logger.info("Function called for wrong method name")
        exit(1)

    return response, uri_client


@pytest.mark.worker
@pytest.mark.worker_retrieve
@pytest.mark.test_worker_retrieve
@pytest.mark.listener
@pytest.mark.sdk
def test_worker_retrieve(setup_config):
    request_file = os.path.join(
        constants.worker_input_file,
        "worker_retrieve.json")

    pre_test_response, uri_client = pre_test(
        read_config(request_file), setup_config)

    output_obj, action_obj = process_input(
        read_config(request_file), pre_test_response=pre_test_response)

    if constants.direct_test_mode == "listener":
        response = submit_request(
            uri_client, output_obj,
            constants.worker_retrieve_output_json_file_name)
    else:
        response = submit_retrieve_sdk(
            output_obj, read_config(request_file))

    assert (check_worker_retrieve_response(response)
            is TestStep.SUCCESS.value)

    logger.info('\t\t!!! Test completed !!!\n\n')
