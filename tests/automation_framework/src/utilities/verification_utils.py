import json
import logging
import crypto_utils.signature as signature
import crypto_utils.crypto_utility as enclave_helper
from error_code.error_status import SignatureStatus
from error_code.error_status import WorkOrderStatus
from src.utilities.generic_utils import TestStep

logger = logging.getLogger(__name__)


def validate_response_code(response):
    """ Function to validate work order response.
        Input Parameters : response, check_result
        Returns : err_cd"""
    # check expected key of test case
    check_result = {"error": {"code": 5}}
    check_result_key = list(check_result.keys())[0]
    # check response code
    if check_result_key in response:
        if "code" in check_result[check_result_key].keys():
            if "code" in response[check_result_key].keys():
                if (response[check_result_key]["code"] ==
                        check_result[check_result_key]["code"]):
                    err_cd = 0
                    logger.info('SUCCESS: WorkOrderSubmit response'
                                ' key (%s) and status (%s)!!\
                                 \n', check_result_key,
                                check_result[check_result_key]["code"])
                elif (response[check_result_key]["code"] ==
                        WorkOrderStatus.INVALID_PARAMETER_FORMAT_OR_VALUE):
                    err_cd = 0
                    logger.info('Invalid parameter format in response "%s".',
                                response[check_result_key]["message"])
                elif (response[check_result_key]["code"] ==
                        WorkOrderStatus.SUCCESS):
                    err_cd = 0
                    logger.info('SUCCESS: Worker API response "%s"!!',
                                response[check_result_key]["message"])
                else:
                    err_cd = 1
                    logger.info('ERROR: Response did not contain expected \
                            %s code %s. \n', check_result_key,
                                check_result[check_result_key]["code"])
            else:
                err_cd = 1
                logger.info('ERROR: Response did not contain %s code \
                           where expected. \n', check_result_key)
    else:
        check_get_result = '''{"result": {"workOrderId": "", "workloadId": "",
                        "workerId": "", "requesterId": "", "workerNonce": "",
                               "workerSignature": "", "outData": ""}}'''

        check_result = json.loads(check_get_result)

        check_result_key = list(check_result.keys())[0]

        if check_result_key == "result":
            if (set(check_result["result"].keys()).issubset
               (response["result"].keys())):

                # Expected Keys : check_result["result"].keys()
                # Actual Keys : response["result"].keys()
                err_cd = 0
                logger.info('SUCCESS: WorkOrderGetResult '
                            'response has keys as expected!!')
            else:
                err_cd = 1
                logger.info('ERROR: Response did not contain keys \
                as expected in for test case. ')
        else:
            err_cd = 0
            logger.info('No validation performed for the expected result \
            in validate response. ')

    return err_cd


def is_valid_params(request_elements, keys_count=None):
    """
    Fucntion to check the number of parameters in submit requests.
    """
    if keys_count:
        request_keys = sum(keys_count(elem) for elem in request_elements)
    return request_keys


def verify_work_order_signature(response, worker_obj):
    verify_key = worker_obj.verification_key

    try:
        verify_obj = signature.ClientSignature()
        sig_bool = verify_obj.verify_signature(response, verify_key)

        if sig_bool is SignatureStatus.PASSED:
            err_cd = 0
            logger.info('Success: Work Order Signature Verified.')
        else:
            err_cd = 1
            logger.info('ERROR: Work Order Signature Verification Failed')
    except Exception:
        err_cd = 1
        logger.error('ERROR: Failed to analyze Signature Verification')

    return err_cd


def decrypt_work_order_response(response, session_key, session_iv):
    decrypted_data = ""
    try:
        decrypted_data = enclave_helper.decrypted_response(response,
                                                           session_key,
                                                           session_iv)
        err_cd = 0
        logger.info('Success: Work Order Response Decrypted.\n\n')
    except Exception:
        err_cd = 1
        logger.info('ERROR: Decryption failed %s \
                           where expected. \n', decrypted_data)
        logger.info('ERROR: Work Order Response Decryption Failed')

    return err_cd, decrypted_data


def response_signature_verification(response, worker_obj, work_order_obj):

    session_key = work_order_obj.session_key
    session_iv = work_order_obj.session_iv

    verify_wo_signature_err = verify_work_order_signature(response,
                                                          worker_obj)

    assert (verify_wo_signature_err is TestStep.SUCCESS.value)

    decrypt_wo_response_err = decrypt_work_order_response(response,
                                                          session_key,
                                                          session_iv)[0]

    assert (decrypt_wo_response_err is TestStep.SUCCESS.value)

    # WorkOrderGetResult API Response validation with key parameters
    validate_response_code_err = validate_response_code(response)

    assert (validate_response_code_err is TestStep.SUCCESS.value)

    return TestStep.SUCCESS.value


def check_worker_lookup_response(response):

    if response["result"]["totalCount"] > 0:
        err_cd = 0
    else:
        err_cd = 1

    return err_cd


def check_worker_retrieve_response(response):

    if response["result"]["workerType"] == 1:

        err_cd = 0
    else:
        err_cd = 1

    return err_cd
