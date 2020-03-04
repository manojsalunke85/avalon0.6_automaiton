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
    import check_worker_lookup_response
from src.libs.avalon_test_wrapper \
    import read_json, submit_request
from src.utilities.generic_utils import TestStep
import operator
from src.libs.test_base import TestBase

logger = logging.getLogger(__name__)


class TestClass():
    test_obj = TestBase()

    @pytest.mark.worker
    @pytest.mark.worker_lookup
    @pytest.mark.test_worker_lookup
    @pytest.mark.listener
    @pytest.mark.sdk
    @pytest.mark.p1
    def test_worker_lookup(self):
        request_file = os.path.join(
            constants.worker_input_file,
            "worker_lookup.json")

        err_cd = self.test_obj.setup_and_build_request_lookup(
            read_json(request_file))

        response = submit_request(
            self.test_obj.uri_client,
            self.test_obj.build_request_output['request_obj'],
            constants.worker_lookup_output_json_file_name,
            read_json(request_file))

        logger.info("**********Received Response*********\n%s\n", response)

        assert (check_worker_lookup_response(response, operator.gt, 0)
                is TestStep.SUCCESS.value)

        self.test_obj.teardown()

        logger.info('\t\t!!! Test completed !!!\n\n')

    @pytest.mark.worker
    @pytest.mark.worker_lookup
    @pytest.mark.test_worker_lookup_workerType_not_unsigned_int
    @pytest.mark.listener
    def test_worker_lookup_workerType_not_unsigned_int(self):
        request_file = os.path.join(
            constants.worker_input_file,
            "worker_lookup_workerType_not_unsigned_int.json")

        err_cd = self.test_obj.setup_and_build_request_lookup(
            read_json(request_file))

        response = submit_request(
            self.test_obj.uri_client,
            self.test_obj.build_request_output['request_obj'],
            constants.worker_lookup_output_json_file_name,
            read_json(request_file))

        logger.info("**********Received Response*********\n%s\n", response)

        assert (check_worker_lookup_response(response, operator.eq, 0)
                is TestStep.SUCCESS.value)

        logger.info('\t\t!!! Test completed !!!\n\n')

    @pytest.mark.worker
    @pytest.mark.worker_lookup
    @pytest.mark.test_worker_lookup_empty_params
    @pytest.mark.listener
    def test_worker_lookup_empty_params(self):
        request_file = os.path.join(
            constants.worker_input_file,
            "worker_lookup_empty_params.json")

        err_cd = self.test_obj.setup_and_build_request_lookup(
            read_json(request_file))

        response = submit_request(
            self.test_obj.uri_client,
            self.test_obj.build_request_output['request_obj'],
            constants.worker_lookup_output_json_file_name,
            read_json(request_file))

        logger.info("**********Received Response*********\n%s\n", response)

        assert (check_worker_lookup_response(response, operator.gt, 0)
                is TestStep.SUCCESS.value)

        logger.info('\t\t!!! Test completed !!!\n\n')

    @pytest.mark.worker
    @pytest.mark.worker_lookup
    @pytest.mark.test_worker_lookup_jsonrpc_different_version
    @pytest.mark.listener
    @pytest.mark.sdk
    def test_worker_lookup_jsonrpc_different_version(self):
        request_file = os.path.join(
            constants.worker_input_file,
            "worker_lookup_jsonrpc_different_version.json")

        err_cd = self.test_obj.setup_and_build_request_lookup(
            read_json(request_file))

        response = submit_request(
            self.test_obj.uri_client,
            self.test_obj.build_request_output['request_obj'],
            constants.worker_lookup_output_json_file_name,
            read_json(request_file))

        logger.info("**********Received Response*********\n%s\n", response)

        assert (check_worker_lookup_response(response, operator.gt, 0)
                is TestStep.SUCCESS.value)

        logger.info('\t\t!!! Test completed !!!\n\n')
