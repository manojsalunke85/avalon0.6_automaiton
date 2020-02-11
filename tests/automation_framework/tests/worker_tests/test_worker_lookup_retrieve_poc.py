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
    import check_worker_lookup_response, check_worker_retrieve_response
from src.libs.avalon_test_wrapper \
    import read_json, run_test
from src.utilities.generic_utils import TestStep
logger = logging.getLogger(__name__)


@pytest.mark.worker
@pytest.mark.worker_lookup
def test_worker_lookup(setup_config):
    """ Testing worker lookup request with all valid parameter values. """

    # retrieve values from conftest session fixture
    request_file = os.path.join(
        constants.worker_input_file,
        "worker_lookup.json")

    input_json_obj = read_json(request_file)

    response = run_test(input_json_obj, setup_config)

    assert (check_worker_lookup_response(response) is TestStep.SUCCESS.value)

    logger.info('\t\t!!! Test completed !!!\n\n')


@pytest.mark.worker
@pytest.mark.worker_retrieve
def test_worker_retrieve(setup_config):
    """ Testing worker retrieve  request with all valid parameter values. """

    # retrieve values from conftest session fixture

    request_file = os.path.join(
        constants.worker_input_file,
        "worker_retrieve.json")

    input_json_obj = read_json(request_file)

    response = run_test(input_json_obj, setup_config)

    assert (check_worker_retrieve_response(response) is TestStep.SUCCESS.value)

    logger.info('\t\t!!! Test completed !!!\n\n')
