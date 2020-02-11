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
import json

from automation_framework.utilities.post_request import \
    post_request
from automation_framework.utilities.request_args import TestStep
from automation_framework.utilities.workflow import validate_response_code

logger = logging.getLogger(__name__)


def test_worker_lookup_workerType_not_unsigned_int(setup_config):
    """ Testing worker lookup for
     invalid worker type by using not unsigned integer. """

    # retrieve values from conftest session fixture
    worker_obj, uri_client, private_key, err_cd = setup_config[:4]
    # input and output names
    request = './worker_tests/input' \
              '/worker_lookup_workerType_not_unsigned_int.json'
    request_mode = 'file'
    output_json_file_name = 'worker_lookup_workerType_not_unsigned_int'
    tamper = {"params": {}}
    request_method = ""
    request_id = 0

    # submit worker lookup
    request_tup = (request, request_mode,
                   tamper, output_json_file_name,
                   uri_client, request_method,
                   worker_obj,
                   request_id)

    response_tup = post_request(request_tup)

    response = response_tup[1]
    # check worker lookup response
    if response["result"]["totalCount"] == 0:
        err_cd = 0
    else:
        err_cd = 1

    assert err_cd == TestStep.SUCCESS.value
    logger.info('\t\t!!! Test completed !!!\n\n')


def test_worker_lookup_empty_params(setup_config):
    """Testing worker lookup with empty
     parameter and validate the  response . """

    # retrieve values from conftest session fixture
    worker_obj, uri_client, private_key, err_cd = setup_config[:4]
    # input and output names
    request = './worker_tests/input/worker_lookup_empty_params.json'
    request_mode = 'file'
    output_json_file_name = 'worker_lookup_empty_params'
    tamper = {"params": {}}
    request_method = ""
    request_id = 0

    # submit worker lookup
    request_tup = (request, request_mode, tamper,
                   output_json_file_name,
                   uri_client, request_method,
                   worker_obj,
                   request_id)

    response_tup = post_request(request_tup)

    response = response_tup[1]
    # check worker lookup response
    if response["result"]["totalCount"] > 0:
        err_cd = 0
    else:
        err_cd = 1

    assert err_cd == TestStep.SUCCESS.value
    logger.info('\t\t!!! Test completed !!!\n\n')


def test_worker_lookup_jsonrpc_different_version(setup_config):
    """ Testing the worker lookup
    request by modifying jsonrpc version. """

    # retrieve values from conftest session fixture
    worker_obj, uri_client, private_key, err_cd = setup_config[:4]
    # input and output names
    request = './worker_tests/input' \
              '/worker_lookup_jsonrpc_different_version.json'

    request_mode = 'file'
    output_json_file_name = 'worker_lookup_jsonrpc_different_version'
    tamper = {"params": {}}
    request_method = ""
    request_id = 0

    # submit worker lookup
    request_tup = (request, request_mode, tamper,
                   output_json_file_name,
                   uri_client, request_method,
                   worker_obj,
                   request_id)

    response_tup = post_request(request_tup)

    response = response_tup[1]
    # check worker lookup response
    if response["result"]["totalCount"] > 0:
        err_cd = 0
    else:
        err_cd = 1

    assert err_cd == TestStep.SUCCESS.value
    logger.info('\t\t!!! Test completed !!!\n\n')
