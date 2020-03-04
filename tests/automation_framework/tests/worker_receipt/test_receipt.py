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
from src.libs.avalon_test_wrapper \
    import read_json, submit_request
from src.utilities.generic_utils import TestStep
from src.utilities.verification_utils \
    import verify_test, validate_response_code
from src.libs.test_base import TestBase

logger = logging.getLogger(__name__)


class TestClass():
    test_obj = TestBase()

    @pytest.mark.work_order_create_receipt
    @pytest.mark.test_work_order_create_receipt
    @pytest.mark.listener
    @pytest.mark.sdk
    @pytest.mark.p1
    def test_work_order_create_receipt(self):
        request_file = os.path.join(
            constants.work_order_receipt,
            "work_order_receipt.json")

        err_cd = self.test_obj.setup_and_build_request_receipt(
            read_json(request_file))

        receipt_response = submit_request(
            self.test_obj.uri_client,
            self.test_obj.build_request_output['request_obj'],
            constants.wo_submit_output_json_file_name,
            read_json(request_file))

        assert (validate_response_code(receipt_response, 2)
                is TestStep.SUCCESS.value)
        logger.info('\t\t!!! Test completed !!!\n\n')

    @pytest.mark.work_order_create_receipt
    @pytest.mark.test_create_work_order_receipt_invalid_requester_id
    @pytest.mark.listener
    @pytest.mark.sdk
    def test_create_work_order_receipt_invalid_requester_id(self):
        request_file = os.path.join(
            constants.work_order_receipt,
            "work_order_receipt_invalid_requester_id.json")

        err_cd = self.test_obj.setup_and_build_request_receipt(
            read_json(request_file))

        receipt_response = submit_request(
            self.test_obj.uri_client,
            self.test_obj.build_request_output['request_obj'],
            constants.wo_submit_output_json_file_name,
            read_json(request_file))

        assert (validate_response_code(receipt_response, 2)
                is TestStep.SUCCESS.value)
        logger.info('\t\t!!! Test completed !!!\n\n')

    @pytest.mark.work_order_create_receipt
    @pytest.mark.test_create_work_order_receipt_hexstr_workorderRequesthash
    @pytest.mark.listener
    @pytest.mark.sdk
    def test_create_work_order_receipt_hexstr_workorderRequesthash(
            self):
        request_file = os.path.join(
            constants.work_order_receipt,
            "work_order_receipt_hexstr_workorderRequesthash.json")

        err_cd = self.test_obj.setup_and_build_request_receipt(
            read_json(request_file))

        receipt_response = submit_request(
            self.test_obj.uri_client,
            self.test_obj.build_request_output['request_obj'],
            constants.wo_submit_output_json_file_name,
            read_json(request_file))

        assert (validate_response_code(receipt_response, 2)
                is TestStep.SUCCESS.value)
        logger.info('\t\t!!! Test completed !!!\n\n')

    @pytest.mark.work_order_create_receipt
    @pytest.mark.test_create_work_order_receipt_wrong_rverificationkey
    @pytest.mark.listener
    @pytest.mark.sdk
    def test_create_work_order_receipt_wrong_rverificationkey(self):
        request_file = os.path.join(
            constants.work_order_receipt,
            "work_order_receipt_wrong_rverificationkey.json")

        err_cd = self.test_obj.setup_and_build_request_receipt(
            read_json(request_file))

        receipt_response = submit_request(
            self.test_obj.uri_client,
            self.test_obj.build_request_output['request_obj'],
            constants.wo_submit_output_json_file_name,
            read_json(request_file))

        assert (validate_response_code(receipt_response, 2)
                is TestStep.SUCCESS.value)
        logger.info('\t\t!!! Test completed !!!\n\n')

    @pytest.mark.work_order_create_receipt
    @pytest.mark.test_create_work_order_receipt_wrong_rverificationkey
    def test_create_work_order_receipt_wrong_rverificationkey(self):
        request_file = os.path.join(
            constants.work_order_receipt,
            "work_order_receipt_wrong_rverificationkey.json")

        err_cd = self.test_obj.setup_and_build_request_receipt(
            read_json(request_file))

        receipt_response = submit_request(
            self.test_obj.uri_client,
            self.test_obj.build_request_output['request_obj'],
            constants.wo_submit_output_json_file_name,
            read_json(request_file))

        assert (validate_response_code(receipt_response, 2)
                is TestStep.SUCCESS.value)
        logger.info('\t\t!!! Test completed !!!\n\n')
