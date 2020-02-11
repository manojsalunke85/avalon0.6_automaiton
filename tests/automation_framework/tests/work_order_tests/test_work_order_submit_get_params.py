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


def test_work_order_submit_requesterNonce_all_special_characters(setup_config):
    """ Testing work order request by submiting
    requesterNonce with special characters. """

    # input file name
    request = 'work_order_tests/input' \
              '/work_order_submit_requesterNonce_all_special_characters.json'

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


def test_work_order_workerEncryptionKey_special_character(setup_config):
    """ Testing work order request by submiting
    worker encryption key with special characters. """

    # input file name
    request = 'work_order_tests/input' \
              '/work_order_workerEncryptionKey_special_character.json'

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


def test_work_order_with_alternate_worker_signing_algorithm(setup_config):
    """ Testing work order request
    by submiting alternate signing algorithm. """

    # input file name
    request = 'work_order_tests/input' \
              '/work_order_with_alternate_worker_signing_algorithm.json'

    work_order_response, generic_params = (work_order_request_params
                                           (setup_config, request))
    err_cd, work_order_get_result_response = (work_order_get_result_params
                                              (work_order_response[:6],
                                               generic_params))

    setup_config[0].signingAlgorithm = "RSA-OAEP-3072"

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


def test_work_order_with_alternate_hashing_algorithm(setup_config):
    """ Testing work order request by
    submiting alternate hashing algorithm. """

    # input file name
    request = 'work_order_tests/input' \
              '/work_order_with_alternate_hashing_algorithm.json'

    work_order_response, generic_params = (work_order_request_params
                                           (setup_config, request))
    err_cd, work_order_get_result_response = (work_order_get_result_params
                                              (work_order_response[:6],
                                               generic_params))

    setup_config[0].hashingAlgorithm = "SHA-512"

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


def test_work_order_without_requester_private_key(setup_config):
    """ Testing work order request by
    submiting without requester private key. """

    # input file name
    request = 'work_order_tests/input' \
              '/work_order_without_requester_private_key.json'
    private_key = ""

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


def test_work_order_submit_twice_params(setup_config):
    """ Testing work order request by passing the
    parameters twice in the request. """

    # input file name
    request = 'work_order_tests/input' \
              '/work_order_submit_twice_params.json'

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


def test_work_order_invalid_parameter(setup_config):
    """ Testing work order request by passing wrong workloadid. """

    # input file name
    request = 'work_order_tests/input' \
              '/work_order_invalid_parameter.json'

    work_order_response, generic_params = (work_order_request_params
                                           (setup_config, request))
    err_cd, work_order_get_result_response = (work_order_get_result_params
                                              (work_order_response[:6],
                                               generic_params))

    # WorkOrderGetResult API Response validation with key parameters
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)


def test_work_order_signature_with_wrong_payload_format(setup_config):
    """ Testing work order request by passing wrong payload format. """

    # input file name
    request = 'work_order_tests/input' \
              '/work_order_signature_with_wrong_payload_format.json'

    work_order_response, generic_params = (work_order_request_params
                                           (setup_config, request))
    err_cd, work_order_get_result_response = (work_order_get_result_params
                                              (work_order_response[:6],
                                               generic_params))

    # WorkOrderGetResult API Response validation with key parameters
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)


def test_work_order_submit_requesterId_param_remove(setup_config):
    """ Testing work order request without requesterId. """

    # input file name
    request = 'work_order_tests/input' \
              '/work_order_submit_requesterId_param_remove.json'

    work_order_response, generic_params = (work_order_request_params
                                           (setup_config, request))
    err_cd, work_order_get_result_response = (work_order_get_result_params
                                              (work_order_response[:6],
                                               generic_params))

    # WorkOrderGetResult API Response validation with key parameters
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)


def test_work_order_submit_workload_id_hex_string(setup_config):
    """ Testing work order request valid hex string workloadid. """

    # input file name
    request = 'work_order_tests/input' \
              '/work_order_submit_workload_id_hex_string.json'
    tamper = {"params": {"before_sign": {"workloadId": ""}}}

    work_order_response, generic_params = (work_order_request_params
                                           (setup_config, request))
    err_cd, work_order_get_result_response = (work_order_get_result_params
                                              (work_order_response[:6],
                                               generic_params))

    # WorkOrderGetResult API Response validation with key parameters
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)


def test_work_order_submit_workload_id_random_string(setup_config):
    """ Test work order request with wrong workload id """

    # input file name
    request = 'work_order_tests/input' \
              '/work_order_submit_workload_id_random_string.json'
    tamper = {"params": {"before_sign": {"workloadId": ""}}}

    work_order_response, generic_params = (work_order_request_params
                                           (setup_config, request))
    err_cd, work_order_get_result_response = (work_order_get_result_params
                                              (work_order_response[:6],
                                               generic_params))

    # WorkOrderGetResult API Response validation with key parameters
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)


def test_work_order_workloadId_specialcharacters(setup_config):
    """ Test work order request with wrong workload id """

    # input file name
    request = 'work_order_tests/input' \
              '/work_order_workloadId_specialcharacters.json'

    work_order_response, generic_params = (work_order_request_params
                                           (setup_config, request))
    err_cd, work_order_get_result_response = (work_order_get_result_params
                                              (work_order_response[:6],
                                               generic_params))

    # WorkOrderGetResult API Response validation with key parameters
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)


def test_work_order_with_not_supported_dataencryption_algorithm(setup_config):
    """ Test work order request with  unsupported dataencryption algorithm  """

    # input file name
    request = 'work_order_tests/input' \
              '/work_order_with_not_supported_dataEncryption_algorithm.json'

    work_order_response, generic_params = (work_order_request_params
                                           (setup_config, request))
    err_cd, work_order_get_result_response = (work_order_get_result_params
                                              (work_order_response[:6],
                                               generic_params))

    # WorkOrderGetResult API Response validation with key parameters
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)


def test_work_order_with_wrong_worker_signing_algorithm(setup_config):
    """ Testing work order request with wrong signing algorithm. """

    # input file name
    request = 'work_order_tests/input' \
              '/work_order_with_wrong_worker_signing_algorithm.json'

    work_order_response, generic_params = (work_order_request_params
                                           (setup_config, request))
    err_cd, work_order_get_result_response = (work_order_get_result_params
                                              (work_order_response[:6],
                                               generic_params))

    setup_config[0].signingAlgorithm = "SECP128K1"

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


def test_work_order_with_empty_dataEncryption_algorithm(setup_config):
    """ Testing work order request by passing
     empty dataencryption algorithm. """

    # input file name
    request = 'work_order_tests/input' \
              '/work_order_with_empty_dataEncryption_algorithm.json'

    work_order_response, generic_params = (work_order_request_params
                                           (setup_config, request))
    err_cd, work_order_get_result_response = (work_order_get_result_params
                                              (work_order_response[:6],
                                               generic_params))

    # WorkOrderGetResult API Response validation with key parameters
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)
    logger.info('\t\t!!! Test completed !!!\n\n')


def test_work_order_with_wrong_requester_signature(setup_config):
    """ Testing work order request by passing
     wrong requester signature. """

    # input file name
    request = 'work_order_tests/input' \
              '/work_order_with_empty_requester_signature.json'
    tamper = {"params": {"after_sign": {"requesterSignature": ""}}}
    work_order_response, generic_params = (work_order_request_params
                                           (setup_config, request))
    err_cd, work_order_get_result_response = (work_order_get_result_params
                                              (work_order_response[:6],
                                               generic_params))

    # WorkOrderGetResult API Response validation with key parameters
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)
    logger.info('\t\t!!! Test completed !!!\n\n')


def test_work_order_with_wrong_private_key(setup_config):
    """ Testing work order request by passing
     wrong private key. """

    # input file name
    request = 'work_order_tests/input' \
              '/work_order_with_wrong_private_key.json'
    private_key = "BA12"
    work_order_response, generic_params = (work_order_request_params
                                           (setup_config, request))
    err_cd, work_order_get_result_response = (work_order_get_result_params
                                              (work_order_response[:6],
                                               generic_params))

    # WorkOrderGetResult API Response validation with key parameters
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)
    logger.info('\t\t!!! Test completed !!!\n\n')


def test_work_order_worker_encryption_key(setup_config):
    """ Testing work order request by passing
     workerencryptionkey. """

    # input file name
    request = 'work_order_tests/input' \
              '/work_order_worker_encryption_key.json'

    work_order_response, generic_params = (work_order_request_params
                                           (setup_config, request))
    err_cd, work_order_get_result_response = (work_order_get_result_params
                                              (work_order_response[:6],
                                               generic_params))

    # WorkOrderGetResult API Response validation with key parameters
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)
    logger.info('\t\t!!! Test completed !!!\n\n')


def test_work_order_submit_WorkOrderId_null(setup_config):
    """ Testing work order request by passing
     empty indata and outdata. """

    # input file name
    request = 'work_order_tests/input' \
              '/work_order_submit_WorkOrderId_null.json'
    tamper = {"params": {"after_sign": {"workOrderId": ""}}}

    work_order_response, generic_params = (work_order_request_params
                                           (setup_config, request))
    err_cd, work_order_get_result_response = (work_order_get_result_params
                                              (work_order_response[:6],
                                               generic_params))

    # WorkOrderGetResult API Response validation with key parameters
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)
    logger.info('\t\t!!! Test completed !!!\n\n')


def test_work_order_submit_requesterId_som_special_characters(setup_config):
    """ Testing work order request for
     requester Id with special_characters. """

    # input file name
    request = 'work_order_tests/input' \
              '/work_order_requesterId_special_characters.json'
    work_order_response, generic_params = (work_order_request_params
                                           (setup_config, request))
    err_cd, work_order_get_result_response = (work_order_get_result_params
                                              (work_order_response[:6],
                                               generic_params))

    # WorkOrderGetResult API Response validation with key parameters
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)
    logger.info('\t\t!!! Test completed !!!\n\n')


def test_work_order_signing_wrong(setup_config):
    """ Testing work order with wrong signature. """

    # input file name
    request = 'work_order_tests/input' \
              '/work_order_signing_wrong.json'
    tamper = {"params": {"after_sign": {"requesterSignature": "hs"}}}
    work_order_response, generic_params = (work_order_request_params
                                           (setup_config, request))
    err_cd, work_order_get_result_response = (work_order_get_result_params
                                              (work_order_response[:6],
                                               generic_params))

    # WorkOrderGetResult API Response validation with key parameters
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)
    logger.info('\t\t!!! Test completed !!!\n\n')


def test_work_order_empty_workloadid(setup_config):
    """ Testing work order request by passing empty workloadid. """

    # input file name
    request = 'work_order_tests/input' \
              '/work_order_only_workloadid.json'

    work_order_response, generic_params = work_order_request_params(
        setup_config, request)

    err_cd, work_order_get_result_response = work_order_get_result_params(
        work_order_response[:2], generic_params)

    # WorkOrderGetResult API Response validation with key parameters
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)
    logger.info('\t\t!!! Test completed !!!\n\n')


def test_work_order_two_workloadid(setup_config):
    """ Testing work order request by passing empty workloadid. """

    # input file name
    request = 'work_order_tests/input' \
              '/work_order_two_workloadid.json'

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


def test_work_order_twice_get_result(setup_config):
    """ Testing work order request by passing diff workload
    with workorder twice and get result. """

    # input file name
    request = 'work_order_tests/input' \
              '/work_order_heartdisease.json'

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
    request = 'work_order_tests/input' \
              '/work_order_echoclient.json'

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


def test_work_order_twice_get_result_same_workload(setup_config):
    """ Testing work order request by passing same workload with
    workorder twice and get result. """

    # input file name
    request = 'work_order_tests/input' \
              '/work_order_heartdisease.json'

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
    request = 'work_order_tests/input' \
              '/work_order_heartdisease.json'

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


def test_work_order_thrice_get_result_same_workload(setup_config):
    """ Testing work order request by passing workorder
    thrice with alternate workload and get result. """

    # input file name
    request = 'work_order_tests/input' \
              '/work_order_heartdisease.json'

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
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)
    request = 'work_order_tests/input' \
              '/work_order_echoclient.json'

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
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)

    request = 'work_order_tests/input' \
              '/work_order_heartdisease.json'

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
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)
    logger.info('\t\t!!! Test completed !!!\n\n')


def test_work_order_four_get_result_same_workload(setup_config):
    """ Testing work order request by passing workorder four
    twice with alternate workload and get result. """

    # input file name
    request = 'work_order_tests/input' \
              '/work_order_heartdisease.json'

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
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)

    request = 'work_order_tests/input' \
              '/work_order_echoclient.json'

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
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)
    request = 'work_order_tests/input' \
              '/work_order_heartdisease.json'

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
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)
    request = 'work_order_tests/input' \
              '/work_order_echoclient.json'

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
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)

    logger.info('\t\t!!! Test completed !!!\n\n')


def test_work_order_not_supported_data_encryption_algorithm_echo(setup_config):
    """ Testing work order request by passing
    invalid indata. """

    # input file name
    request = 'work_order_tests/input' \
              '/work_order_non_supported_dataalgorithm_echoclient.json'

    work_order_response, generic_params = work_order_request_params(
        setup_config, request)

    err_cd, work_order_get_result_response = work_order_get_result_params(
        work_order_response[:2], generic_params)

    # WorkOrderGetResult API Response validation with key parameters
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)
    logger.info('\t\t!!! Test completed !!!\n\n')


def test_work_order_multiple_dataEncryptionAlgorithm(setup_config):
    """ Testing work order request by passing
     multiple data encryption algorithm. """
    request = 'work_order_tests/input' \
              '/work_order_multiple_dataEncryptionAlgorithm.json'

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
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)
    logger.info('\t\t!!! Test completed !!!\n\n')


def test_work_order_two_workloadid_echoclient(setup_config):
    """ Testing work order request by passing heart
    workloadid and echoclient workload in one workorder. """

    # input file name
    request = 'work_order_tests/input' \
              '/work_order_two_workloadid_echoclient.json'

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


def test_work_order_pformate_list(setup_config):
    """ Testing work order request by passing
    pforamte list. """

    # input file name
    request = 'work_order_tests/input' \
              '/test_work_order_pformate_list.json'

    work_order_response, generic_params = work_order_request_params(
        setup_config, request)

    err_cd, work_order_get_result_response = work_order_get_result_params(
        work_order_response[:2], generic_params)

    # WorkOrderGetResult API Response validation with key parameters
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)
    logger.info('\t\t!!! Test completed !!!\n\n')


def test_work_order_response_timeout_str(setup_config):
    """ Testing work order request by passing string
    is response timeout. """
    # input file name
    request = 'work_order_tests/input' \
              '/work_order_response_timeout_str.json'

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


def test_work_order_remove_payload_format_echoclient(setup_config):
    """ Testing work order request by removal of payload format. """

    # input file name
    request = 'work_order_tests/input' \
              '/work_order_remove_payload_format_echoclient.json'

    work_order_response, generic_params = work_order_request_params(
        setup_config, request)

    err_cd, work_order_get_result_response = work_order_get_result_params(
        work_order_response[:2], generic_params)

    # WorkOrderGetResult API Response validation with key parameters
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)
    logger.info('\t\t!!! Test completed !!!\n\n')


def test_work_order_twice_getresult_twice(setup_config):
    """ Testing work order request by passing """

    # input file name
    request = 'work_order_tests/input' \
              '/work_order_heartdisease.json'

    work_order_response, generic_params = work_order_request_params(
        setup_config, request)
    request = 'work_order_tests/input' \
              '/work_order_echoclient.json'

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


def test_workorder_thrice_getresult_thrice(setup_config):
    """ Testing work order request by passing workorder
    then get result thrice """

    # input file name
    request = 'work_order_tests/input' \
              '/work_order_heartdisease.json'

    work_order_response, generic_params = work_order_request_params(
        setup_config, request)
    request = 'work_order_tests/input' \
              '/work_order_echoclient.json'

    work_order_response, generic_params = work_order_request_params(
        setup_config, request)
    request = 'work_order_tests/input' \
              '/work_order_heartdisease.json'

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


def test_work_order_dataEncryptionAlgorithm_list_same_algo_twice(setup_config):
    """ Testing work order request by passing twice
     same data encryption algorithm. """
    # input file name
    request = 'work_order_tests/input' \
              '/work_order_dataEncryptionAlgorithm_list_same_algo_twice.json'

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


def test_work_order_without_id_param(setup_config):
    """ Testing work order request by removal of id. """

    # input file name
    request = 'work_order_tests/input' \
              '/work_order_without_id_param.json'

    work_order_response, generic_params = work_order_request_params(
        setup_config, request)

    err_cd, work_order_get_result_response = work_order_get_result_params(
        work_order_response[:2], generic_params)

    # WorkOrderGetResult API Response validation with key parameters
    assert (validate_response_code(work_order_get_result_response) is
            TestStep.SUCCESS.value)
    logger.info('\t\t!!! Test completed !!!\n\n')
