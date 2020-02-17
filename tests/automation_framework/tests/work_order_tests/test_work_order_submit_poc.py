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
    import response_signature_verification
from src.libs.avalon_test_wrapper \
    import read_json, run_test
from src.utilities.generic_utils import TestStep
logger = logging.getLogger(__name__)


@pytest.mark.work_order
@pytest.mark.work_order_success
def test_work_order_success(setup_config):
    """ Testing work order request with all valid parameter values. """

    # input file name
    logger.info('\t\t!!! Test started !!!\n\n')
    request_file = os.path.join(
        constants.work_order_input_file,
        "work_order_success.json")

    input_json_obj = read_json(request_file)

    (work_order_submit_response, work_order_get_result_response,
     worker_obj, work_order_obj) = run_test(input_json_obj, setup_config)

    assert (response_signature_verification
            (work_order_get_result_response, worker_obj, work_order_obj)
            is TestStep.SUCCESS.value)

    logger.info('\t\t!!! Test completed !!!\n\n')
