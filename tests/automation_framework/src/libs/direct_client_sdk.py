import os
import json
import logging
import secrets
import sys

import config.config as pconfig
import crypto_utils.crypto_utility as crypto_utility
from avalon_client_sdk.utility.tcf_types import WorkerType
import avalon_client_sdk.worker.worker_details as worker_details
from avalon_client_sdk.work_order.work_order_params import WorkOrderParams
from avalon_client_sdk.ethereum.ethereum_worker_registry_list_client import \
    EthereumWorkerRegistryListClientImpl
from avalon_client_sdk.direct.jrpc.worker_registry_jrpc_client import \
    WorkerRegistryJRPCClientImpl
from avalon_client_sdk.direct.jrpc.work_order_jrpc_client import \
    WorkOrderJRPCClientImpl
from avalon_client_sdk.direct.jrpc.work_order_receipt_jrpc_client \
     import WorkOrderReceiptJRPCClientImpl
from error_code.error_status import WorkOrderStatus, ReceiptCreateStatus
import crypto_utils.signature as signature
from error_code.error_status import SignatureStatus
from avalon_client_sdk.work_order_receipt.work_order_receipt_request \
    import WorkOrderReceiptRequest


logger = logging.getLogger(__name__)
TCFHOME = os.environ.get("TCF_HOME", "../../")


def worker_lookup_sdk(jrpc_req_id, input_json=None):
    conffiles = ["tcs_config.toml"]
    confpaths = [".", TCFHOME + "/config", "../../etc"]
    config = pconfig.parse_configuration_files(conffiles, confpaths)

    worker_dict = {'SGX': WorkerType.TEE_SGX,
                   'MPC': WorkerType.MPC, 'ZK': WorkerType.ZK}
    if input_json is None:
        worker_type = 'SGX'
    else:
        try:
            worker_value = input_json["params"]["workerType"]
            if worker_value == 1:
                worker_type = 'SGX'
            elif worker_value == 2:
                worker_type = 'MPC'
            elif worker_value == 3:
                worker_type = 'ZK'
        except LookupError:
            worker_type = ""

    worker_registry = WorkerRegistryJRPCClientImpl(config)

    worker_lookup_response = worker_registry.worker_lookup(
        worker_type=worker_dict[worker_type], id=jrpc_req_id
    )
    logger.info("\n Worker lookup response: {}\n".format(
        json.dumps(worker_lookup_response, indent=4)
    ))

    return worker_lookup_response, worker_registry


def get_worker_id_sdk(worker_lookup_result):
    if "result" in worker_lookup_result and \
            "ids" in worker_lookup_result["result"].keys():
        if worker_lookup_result["result"]["totalCount"] != 0:
            worker_id = worker_lookup_result["result"]["ids"][0]
        else:
            logger.error("ERROR: No workers found")
            worker_id = None
    else:
        logger.error("ERROR: Failed to lookup worker")
        worker_id = None

    return worker_id


def worker_retrieve_details_sdk(worker_registry, jrpc_req_id, worker_id):
    jrpc_req_id += 1
    worker_retrieve_result = worker_registry.worker_retrieve(
        worker_id, jrpc_req_id
    )
    logger.info("\n Worker retrieve response: {}\n".format(
        json.dumps(worker_retrieve_result, indent=4)
    ))

    if "error" in worker_retrieve_result:
        logger.error("Unable to retrieve worker details\n")
        sys.exit(1)

    return worker_retrieve_result


def worker_initialize_sdk(worker_retrieve_result, worker_id):
    # Initializing Worker Object
    worker_obj = worker_details.SGXWorkerDetails()
    worker_obj.load_worker(worker_retrieve_result)

    logger.info("**********Worker details Updated with Worker ID" +
                "*********\n%s\n", worker_id)

    return worker_obj


def _create_work_order_params(input_json_obj, worker_obj):

    # Create session key and iv to sign work order request
    session_key = crypto_utility.generate_key()
    session_iv = crypto_utility.generate_iv()
    logger.info("JSON object %s \n", input_json_obj)
    worker_id = worker_obj.worker_id
    workload_id = input_json_obj["params"]["workloadId"]
    in_data = input_json_obj["params"]["inData"]
    worker_encrypt_key = worker_obj.encryption_key
    logger.info("workload_id %s \n", workload_id)
    # Convert workloadId to hex
    workload_id = workload_id.encode("UTF-8").hex()
    work_order_id = secrets.token_hex(32)
    requester_id = secrets.token_hex(32)
    requester_nonce = secrets.token_hex(16)
    # Create work order params
    wo_params = WorkOrderParams(
        work_order_id, worker_id, workload_id, requester_id,
        session_key, session_iv, requester_nonce,
        result_uri=" ", notify_uri=" ",
        worker_encryption_key=worker_encrypt_key,
        data_encryption_algorithm="AES-GCM-256"
    )
    logger.info("In data %s \n", in_data)
    # Add worker input data
    for rows in in_data:
        for k, v in rows.items():
            if k == "data":
                wo_params.add_in_data(rows["data"])

    # Encrypt work order request hash
    wo_params.add_encrypted_request_hash()

    return wo_params


def create_work_order_receipt(wo_receipt, wo_params,
                              client_private_key, jrpc_req_id):
    # Create work order receipt object using WorkOrderReceiptRequest class
    # This fuction will send WorkOrderReceiptCreate json rpc request
    wo_request = json.loads(wo_params.to_jrpc_string(jrpc_req_id))
    wo_receipt_request_obj = WorkOrderReceiptRequest()
    wo_create_receipt = wo_receipt_request_obj.create_receipt(
        wo_request,
        ReceiptCreateStatus.PENDING.value,
        client_private_key
    )
    logger.info("Work order create receipt request : {} \n \n ".format(
        json.dumps(wo_create_receipt, indent=4)
    ))
    # Submit work order create receipt jrpc request
    wo_receipt_resp = wo_receipt.work_order_receipt_create(
        wo_create_receipt["workOrderId"],
        wo_create_receipt["workerServiceId"],
        wo_create_receipt["workerId"],
        wo_create_receipt["requesterId"],
        wo_create_receipt["receiptCreateStatus"],
        wo_create_receipt["workOrderRequestHash"],
        wo_create_receipt["requesterGeneratedNonce"],
        wo_create_receipt["requesterSignature"],
        wo_create_receipt["signatureRules"],
        wo_create_receipt["receiptVerificationKey"],
        jrpc_req_id
    )
    logger.info("Work order create receipt response : {} \n \n ".format(
        wo_receipt_resp
    ))


def _retrieve_work_order_receipt(wo_receipt, wo_params, jrpc_req_id):
    # Retrieve work order receipt
    receipt_res = wo_receipt.work_order_receipt_retrieve(
                        wo_params.get_work_order_id(),
                        id=jrpc_req_id
                    )
    logger.info("\n Retrieve receipt response:\n {}".format(
        json.dumps(receipt_res, indent=4)
    ))
    # Retrieve last update to receipt by passing 0xFFFFFFFF
    jrpc_req_id += 1
    receipt_update_retrieve = \
        wo_receipt.work_order_receipt_update_retrieve(
            wo_params.get_work_order_id(),
            None,
            1 << 32,
            id=jrpc_req_id)
    logger.info("\n Last update to receipt receipt is:\n {}".format(
        json.dumps(receipt_update_retrieve, indent=4)
    ))

    return receipt_update_retrieve


def _verify_receipt_signature(receipt_update_retrieve):
    # Verify receipt signature
    sig_obj = signature.ClientSignature()
    status = sig_obj.verify_update_receipt_signature(
        receipt_update_retrieve)
    if status == SignatureStatus.PASSED:
        logger.info(
            "Work order receipt retrieve signature verification " +
            "successful")
    else:
        logger.error(
            "Work order receipt retrieve signature verification failed!!")
        return False

    return True


def _verify_wo_res_signature(work_order_res,
                             worker_verification_key):
    # Verify work order result signature
    sig_obj = signature.ClientSignature()
    status = sig_obj.verify_signature(work_order_res, worker_verification_key)
    if status == SignatureStatus.PASSED:
        logger.info("Signature verification Successful")
    else:
        logger.error("Signature verification Failed")
        return False

    return True


def submit_work_order_client_sdk(input_json_obj, worker_obj):
    wo_params = _create_work_order_params(input_json_obj, worker_obj)
    req_id = input_json_obj["id"]
    conffiles = ["tcs_config.toml"]
    confpaths = [".", TCFHOME + "/config", "../../etc"]
    config = pconfig.parse_configuration_files(conffiles, confpaths)
    work_order = WorkOrderJRPCClientImpl(config)
    response = work_order.work_order_submit(
        wo_params.get_work_order_id(),
        wo_params.get_worker_id(),
        wo_params.get_requester_id(),
        wo_params.to_string(),
        id=req_id
    )
    logger.info("Work order submit response : {}\n ".format(
        json.dumps(response, indent=4)
    ))

    return response, work_order, wo_params


def get_work_order_result_sdk(work_order, wo_params, id):
    work_order_get_result_response = work_order.work_order_get_result(
        wo_params.get_work_order_id(),
        id
    )

    logger.info("Work order get result : {}\n ".format(
        json.dumps(work_order_get_result_response, indent=4)
    ))

    return work_order_get_result_response
