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
    import read_json, submit_request
from src.utilities.generic_utils import TestStep
from src.libs.test_base import TestBase

logger = logging.getLogger(__name__)


class TestClass():
    test_obj = TestBase()

    @pytest.mark.worker
    @pytest.mark.worker_retrieve
    @pytest.mark.test_worker_retrieve
    @pytest.mark.listener
    @pytest.mark.sdk
    @pytest.mark.p1
    def test_worker_retrieve(self):
        request_file = os.path.join(
            constants.worker_input_file,
            "worker_retrieve.json")

        err_cd = self.test_obj.setup_and_build_request_retrieve(
            read_json(request_file))

        submit_response = submit_request(
            self.test_obj.uri_client,
            self.test_obj.build_request_output['request_obj'],
            constants.wo_submit_output_json_file_name,
            read_json(request_file))

        assert (check_worker_retrieve_response(submit_response)
                is TestStep.SUCCESS.value)

        logger.info('\t\t!!! Test completed !!!\n\n')
