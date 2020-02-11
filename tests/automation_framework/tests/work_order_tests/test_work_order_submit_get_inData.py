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
from work_order_tests.work_order_tests import work_order_get_result_params, \
    work_order_request_params
from automation_framework.work_order_submit.work_order_submit_utility \
    import verify_work_order_signature, decrypt_work_order_response
from automation_framework.utilities.request_args import TestStep
from automation_framework.utilities.workflow import validate_response_code

logger = logging.getLogger(__name__)


def test_work_order_inData_DataEncryptionKey_hyphen_echo(setup_config):
    """ Testing work order request by passing hyphen \
    in encrypteddataencryption in indata """

    # input file name
    request = 'work_order_tests/' \
              'input/work_order_inData_DataEncryptionKey_hyphen_echo.json'

    work_order_response, generic_params = (work_order_request_params
                                           (setup_config, request))
    err_cd, work_order_get_result_response = (work_order_get_result_params
                                              (work_order_response[:6],
                                               generic_params))

    if err_cd == 0:
        logger.info('Test Case Success:Work Order Processed successfully '
                    'without decryption as we are passing hyphen in '
                    'encryptedDataEncryptionKey in inData ')
    else:
        logger.info('Test Case Failed : Work Order Not Processed successfully'
                    ' with Signature Verification and Decrypted Response')
    assert err_cd == 0


def test_work_order_data_datahash_null(setup_config):
    """ Testing work order request with data and datahash null. """

    # input file name
    request = 'work_order_tests/input/work_order_data_datahash_null.json'

    work_order_response, generic_params = (work_order_request_params
                                           (setup_config, request))
    err_cd, work_order_get_result_response = (work_order_get_result_params
                                              (work_order_response[:6],
                                               generic_params))

    assert (verify_work_order_signature(work_order_get_result_response,
                                        generic_params[0])
            is TestStep.SUCCESS.value)

    assert (decrypt_work_order_response(work_order_get_result_response,
                                        work_order_response[3],
                                        work_order_response[4])[0]
            is TestStep.SUCCESS.value)

    # WorkOrderGetResult API Response validation with key parameters
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)


def test_work_order_datahash_random_str(setup_config):
    """ Testing work order request by passing random string in datahash"""

    # input file name
    request = 'work_order_tests/input/work_order_datahash_random_str.json'

    work_order_response, generic_params = (work_order_request_params
                                           (setup_config, request))
    err_cd, work_order_get_result_response = (work_order_get_result_params
                                              (work_order_response[:2],
                                               generic_params))

    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)


def test_work_order_indata_index1_data_different_hexlength(setup_config):
    """Testing work order request with indata
    index1 data with different hex length."""

    # input file name
    request = 'work_order_tests/input' \
              '/work_order_indata_index1_data_diff_len.json'

    work_order_response, generic_params = (work_order_request_params
                                           (setup_config, request))
    err_cd, work_order_get_result_response = (work_order_get_result_params
                                              (work_order_response[:6],
                                               generic_params))

    assert (verify_work_order_signature(work_order_get_result_response,
                                        generic_params[0])
            is TestStep.SUCCESS.value)

    assert (decrypt_work_order_response(work_order_get_result_response,
                                        work_order_response[3],
                                        work_order_response[4])[0]
            is TestStep.SUCCESS.value)

    # WorkOrderGetResult API Response validation with key parameters
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)


def test_work_order_submit_requesterId_null(setup_config):
    """ Testing work order request for setting requesterId as null. """

    # input file name
    request = 'work_order_tests/input/work_order_requester_id_null.json'

    work_order_response, generic_params = (work_order_request_params
                                           (setup_config, request))
    err_cd, work_order_get_result_response = (work_order_get_result_params
                                              (work_order_response[:6],
                                               generic_params))

    assert (verify_work_order_signature(work_order_get_result_response,
                                        generic_params[0])
            is TestStep.SUCCESS.value)

    assert (decrypt_work_order_response(work_order_get_result_response,
                                        work_order_response[3],
                                        work_order_response[4])[0]
            is TestStep.SUCCESS.value)

    # WorkOrderGetResult API Response validation with key parameters
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)


def test_work_order_submit_sessionkeyiv_and_iv_indata_hex_string(setup_config):
    """ Testing work order request by setting requesterId as null. """
    # input file name
    request = 'work_order_tests/input/work_order_iv_indata_hex_string.json'

    work_order_response, generic_params = (work_order_request_params
                                           (setup_config, request))
    err_cd, work_order_get_result_response = (work_order_get_result_params
                                              (work_order_response[:6],
                                               generic_params))

    assert (verify_work_order_signature(work_order_get_result_response,
                                        generic_params[0])
            is TestStep.SUCCESS.value)

    assert (decrypt_work_order_response(work_order_get_result_response,
                                        work_order_response[3],
                                        work_order_response[4])[0]
            is TestStep.SUCCESS.value)

    # WorkOrderGetResult API Response validation with key parameters
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)


def test_work_order_specialcharacter_data_single_index_indata(setup_config):
    """Testing work order request with all
    special characters in index of indata """
    # input file name
    request = 'work_order_tests/input' \
              '/work_order_specialcharacter_data_single_index_indata.json'

    work_order_response, generic_params = (work_order_request_params
                                           (setup_config, request))
    err_cd, work_order_get_result_response = (work_order_get_result_params
                                              (work_order_response[:6],
                                               generic_params))

    assert (verify_work_order_signature(work_order_get_result_response,
                                        generic_params[0])
            is TestStep.SUCCESS.value)

    assert (decrypt_work_order_response(work_order_get_result_response,
                                        work_order_response[3],
                                        work_order_response[4])[0]
            is TestStep.SUCCESS.value)

    # WorkOrderGetResult API Response validation with key parameters
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)


def test_work_order_with_changing_order_index(setup_config):
    """Testing work order request with changing order index """
    # input file name
    request = 'work_order_tests/input' \
              '/work_order_with_changing_order_index.json'

    work_order_response, generic_params = (work_order_request_params
                                           (setup_config, request))
    err_cd, work_order_get_result_response = (work_order_get_result_params
                                              (work_order_response[:6],
                                               generic_params))

    assert (verify_work_order_signature(work_order_get_result_response,
                                        generic_params[0])
            is TestStep.SUCCESS.value)

    assert (decrypt_work_order_response(work_order_get_result_response,
                                        work_order_response[3],
                                        work_order_response[4])[0]
            is TestStep.SUCCESS.value)

    # WorkOrderGetResult API Response validation with key parameters
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)


def test_work_order_unknown_parameter(setup_config):
    """Testing work order request with unknow parameter in indata"""
    # input file name
    request = 'work_order_tests/input/work_order_unknown_parameter.json'

    work_order_response, generic_params = (work_order_request_params
                                           (setup_config, request))
    err_cd, work_order_get_result_response = (work_order_get_result_params
                                              (work_order_response[:6],
                                               generic_params))

    assert (verify_work_order_signature(work_order_get_result_response,
                                        generic_params[0])
            is TestStep.SUCCESS.value)

    assert (decrypt_work_order_response(work_order_get_result_response,
                                        work_order_response[3],
                                        work_order_response[4])[0]
            is TestStep.SUCCESS.value)

    # WorkOrderGetResult API Response validation with key parameters
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)


def test_work_order_with_empty_indata_hash(setup_config):
    """Testing work order request with empty indata hash"""
    # input file name
    request = 'work_order_tests/input/work_order_with_empty_indata_hash.json'

    work_order_response, generic_params = (work_order_request_params
                                           (setup_config, request))
    err_cd, work_order_get_result_response = (work_order_get_result_params
                                              (work_order_response[:6],
                                               generic_params))

    assert (verify_work_order_signature(work_order_get_result_response,
                                        generic_params[0])
            is TestStep.SUCCESS.value)

    assert (decrypt_work_order_response(work_order_get_result_response,
                                        work_order_response[3],
                                        work_order_response[4])[0]
            is TestStep.SUCCESS.value)

    # WorkOrderGetResult API Response validation with key parameters
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)


def test_work_order_with_index0_indata(setup_config):
    """Testing work order request with index 0"""

    # input file name
    request = 'work_order_tests/input/work_order_with_index0_indata.json'

    work_order_response, generic_params = (work_order_request_params
                                           (setup_config, request))
    err_cd, work_order_get_result_response = (work_order_get_result_params
                                              (work_order_response[:6],
                                               generic_params))

    assert (verify_work_order_signature(work_order_get_result_response,
                                        generic_params[0])
            is TestStep.SUCCESS.value)

    assert (decrypt_work_order_response(work_order_get_result_response,
                                        work_order_response[3],
                                        work_order_response[4])[0]
            is TestStep.SUCCESS.value)

    # WorkOrderGetResult API Response validation with key parameters
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)


def test_work_order_encryptedDataEncryptionKey_null(setup_config):
    """Testing work order by passing
    encryptedDataEncryptionKey null in index of indata."""

    # input file name
    request = 'work_order_tests/input' \
              '/work_order_encryptedDataEncryptionKey_null.json'

    work_order_response, generic_params = (work_order_request_params
                                           (setup_config, request))
    err_cd, work_order_get_result_response = (work_order_get_result_params
                                              (work_order_response[:6],
                                               generic_params))

    assert (verify_work_order_signature(work_order_get_result_response,
                                        generic_params[0])
            is TestStep.SUCCESS.value)

    assert (decrypt_work_order_response(work_order_get_result_response,
                                        work_order_response[3],
                                        work_order_response[4])[0]
            is TestStep.SUCCESS.value)

    # WorkOrderGetResult API Response validation with key parameters
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)


def test_work_order_indata_outdata(setup_config):
    """Testing work order request with both indata and outdata ."""

    # input file name
    request = 'work_order_tests/input/work_order_indata_outdata.json'

    work_order_response, generic_params = (work_order_request_params
                                           (setup_config, request))
    err_cd, work_order_get_result_response = (work_order_get_result_params
                                              (work_order_response[:6],
                                               generic_params))

    assert (verify_work_order_signature(work_order_get_result_response,
                                        generic_params[0])
            is TestStep.SUCCESS.value)

    assert (decrypt_work_order_response(work_order_get_result_response,
                                        work_order_response[3],
                                        work_order_response[4])[0]
            is TestStep.SUCCESS.value)

    # WorkOrderGetResult API Response validation with key parameters
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)


def test_work_order_negative_index(setup_config):
    """Testing work order by passing negative index in indata."""

    # input file name
    request = 'work_order_tests/input/work_order_negative_index.json'

    work_order_response, generic_params = (work_order_request_params
                                           (setup_config, request))
    err_cd, work_order_get_result_response = (work_order_get_result_params
                                              (work_order_response[:6],
                                               generic_params))

    assert (verify_work_order_signature(work_order_get_result_response,
                                        generic_params[0])
            is TestStep.SUCCESS.value)

    assert (decrypt_work_order_response(work_order_get_result_response,
                                        work_order_response[3],
                                        work_order_response[4])[0]
            is TestStep.SUCCESS.value)

    # WorkOrderGetResult API Response validation with key parameters
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)


def test_work_order_with_50_index_indata(setup_config):
    """Testing work order by passing 50 index in indata."""

    # input file name
    request = 'work_order_tests/input/work_order_with_50_index_indata.json'

    work_order_response, generic_params = (work_order_request_params
                                           (setup_config, request))
    err_cd, work_order_get_result_response = (work_order_get_result_params
                                              (work_order_response[:6],
                                               generic_params))

    assert (verify_work_order_signature(work_order_get_result_response,
                                        generic_params[0])
            is TestStep.SUCCESS.value)

    assert (decrypt_work_order_response(work_order_get_result_response,
                                        work_order_response[3],
                                        work_order_response[4])[0]
            is TestStep.SUCCESS.value)

    # WorkOrderGetResult API Response validation with key parameters
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)


def test_work_order_with_alternate_dataEncryption_algorithm(setup_config):
    """testing work order request by
    passing invalid dataEncryption algorithm ."""

    # input file name
    request = 'work_order_tests/input' \
              '/work_order_with_alternate_dataEncryption_algorithm.json'

    work_order_response, generic_params = (work_order_request_params
                                           (setup_config, request))
    err_cd, work_order_get_result_response = (work_order_get_result_params
                                              (work_order_response[:6],
                                               generic_params))
    check_get_result = {"error": {"code": 2}}

    if err_cd == TestStep.SUCCESS.value:
        logger.info('Test Work Order proceeded successfully ')
    else:
        logger.info('WorkOrderGetResult response has received '
                    'expected result for passing alternate '
                    'data algorithm')


def test_work_order_with_empty_indata(setup_config):
    """testing work order request by
    passing invalid dataEncryption algorithm ."""

    # input file name
    request = 'work_order_tests/input/work_order_with_empty_indata.json'

    work_order_response, generic_params = (work_order_request_params
                                           (setup_config, request))
    err_cd, work_order_get_result_response = (work_order_get_result_params
                                              (work_order_response[:2],
                                               generic_params))

    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)


def test_work_order_with_empty_data_and_datahash_in_indata(setup_config):
    """."""

    # input file name
    request = 'work_order_tests/input' \
              '/work_order_with_empty_data_and_datahash_in_indata.json'

    work_order_response, generic_params = (work_order_request_params
                                           (setup_config, request))
    err_cd, work_order_get_result_response = (work_order_get_result_params
                                              (work_order_response[:6],
                                               generic_params))

    #    assert (verify_work_order_signature(work_order_get_result_response,
    #                                       generic_params[0])
    #           is TestStep.SUCCESS.value)

    #    assert (decrypt_work_order_response(work_order_get_result_response,
    #                                      work_order_response[3],
    #                                     work_order_response[4])[0]
    #        is TestStep.SUCCESS.value)

    # WorkOrderGetResult API Response validation with key parameters
    #  assert (validate_response_code(work_order_get_result_response) is
    #         TestStep.SUCCESS.value)
    if err_cd == TestStep.SUCCESS.value:
        logger.info('Test Work Order proceeded successfully ')
    else:
        logger.info('WorkOrderGetResult response has received '
                    'expected result for passing empty '
                    'indata')


def test_work_order_submit_datahash_calculation(setup_config):
    """ Testing work order request by passing
    required parameters for dataHash calculation. """

    # input file name
    request = 'work_order_tests/input' \
              '/work_order_submit_datahash_calculation.json'

    work_order_response, generic_params = (work_order_request_params
                                           (setup_config, request))
    err_cd, work_order_get_result_response = (work_order_get_result_params
                                              (work_order_response[:6],
                                               generic_params))

    assert (verify_work_order_signature(work_order_get_result_response,
                                        generic_params[0])
            is TestStep.SUCCESS.value)

    assert (decrypt_work_order_response(work_order_get_result_response,
                                        work_order_response[3],
                                        work_order_response[4])[0]
            is TestStep.SUCCESS.value)

    # WorkOrderGetResult API Response validation with key parameters
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)


def test_work_order_multiple_data_echoresult(setup_config):
    """ Testing work order request with multiple data
    in indata using eco-result has workloadid. """

    # input file name
    request = 'work_order_tests/input' \
              '/work_order_multiple_data_echoresult.json'

    work_order_response, generic_params = (work_order_request_params
                                           (setup_config, request))
    err_cd, work_order_get_result_response = (work_order_get_result_params
                                              (work_order_response[:6],
                                               generic_params))

    assert (verify_work_order_signature(work_order_get_result_response,
                                        generic_params[0])
            is TestStep.SUCCESS.value)

    assert (decrypt_work_order_response(work_order_get_result_response,
                                        work_order_response[3],
                                        work_order_response[4])[0]
            is TestStep.SUCCESS.value)

    # WorkOrderGetResult API Response validation with key parameters
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)


def test_work_order_diff_text_data_indata_echoClient(setup_config):
    """ Testing work order request with multiple data in
     indata using echo-result has workloadid. """

    # input file name
    request = 'work_order_tests/input' \
              '/work_order_diff_text_data_indata_echoClient.json'

    work_order_response, generic_params = (work_order_request_params
                                           (setup_config, request))
    err_cd, work_order_get_result_response = (work_order_get_result_params
                                              (work_order_response[:6],
                                               generic_params))

    assert (verify_work_order_signature(work_order_get_result_response,
                                        generic_params[0])
            is TestStep.SUCCESS.value)

    assert (decrypt_work_order_response(work_order_get_result_response,
                                        work_order_response[3],
                                        work_order_response[4])[0]
            is TestStep.SUCCESS.value)

    # WorkOrderGetResult API Response validation with key parameters
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)


def test_work_order_with_no_indata(setup_config):
    """ Testing work order request with no indata """

    # input file name
    request = 'work_order_tests/input/work_order_with_no_indata.json'

    work_order_response, generic_params = (work_order_request_params
                                           (setup_config, request))
    err_cd, work_order_get_result_response = (work_order_get_result_params
                                              (work_order_response[:6],
                                               generic_params))

    assert (verify_work_order_signature(work_order_get_result_response,
                                        generic_params[0])
            is TestStep.SUCCESS.value)

    assert (decrypt_work_order_response(work_order_get_result_response,
                                        work_order_response[3],
                                        work_order_response[4])[0]
            is TestStep.SUCCESS.value)


def test_work_order_encryptedDataEncryptionKey_hyphen(setup_config):
    """ Testing work order by passing
     encryptedDataEncryptionKey hyphen in index of indata. """

    # input file name
    request = 'work_order_tests/input' \
              '/work_order_encryptedDataEncryptionKey_hyphen.json'

    work_order_response, generic_params = work_order_request_params(
        setup_config, request)

    err_cd, work_order_get_result_response = work_order_get_result_params(
        work_order_response[:2], generic_params)

    # WorkOrderGetResult API Response validation with key parameters
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)

    logger.info('\t\t!!! Test completed !!!\n\n')


def test_work_order_with_indata_unknown_parameter_value(setup_config):
    """ Testing work order request by passing
     invalid indata. """

    # input file name
    request = 'work_order_tests/input' \
              '/work_order_with_indata_unknown_parameter_value.json'

    work_order_response, generic_params = work_order_request_params(
        setup_config, request)

    err_cd, work_order_get_result_response = work_order_get_result_params(
        work_order_response[:2], generic_params)

    # WorkOrderGetResult API Response validation with key parameters
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)
    logger.info('\t\t!!! Test completed !!!\n\n')


def test_work_order_params_indata_first(setup_config):
    """ Testing work order request with indata first then params. """

    # input file name
    request = 'work_order_tests/input/work_order_params_indata_first.json'

    work_order_response, generic_params = work_order_request_params(
        setup_config, request)

    err_cd, work_order_get_result_response = work_order_get_result_params(
        work_order_response[:2], generic_params)

    assert (verify_work_order_signature(work_order_get_result_response,
                                        generic_params[0])
            is TestStep.SUCCESS.value)

    assert (decrypt_work_order_response(work_order_get_result_response,
                                        work_order_response[3],
                                        work_order_response[4])[0]
            is TestStep.SUCCESS.value)

    # WorkOrderGetResult API Response validation with key parameters
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)

    logger.info('\t\t!!! Test completed !!!\n\n')


def test_work_order_special_char_iv_echoresult(setup_config):
    """ Testing work order request by passing
     special characters in iv. """

    # input file name
    request = 'work_order_tests/input' \
              '/work_order_special_char_iv_echoresult.json'

    work_order_response, generic_params = work_order_request_params(
        setup_config, request)

    err_cd, work_order_get_result_response = work_order_get_result_params(
        work_order_response[:2], generic_params)

    # WorkOrderGetResult API Response validation with key parameters
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)
    logger.info('\t\t!!! Test completed !!!\n\n')
