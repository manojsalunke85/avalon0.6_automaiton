import logging
import json
import time
import os
import sys
from src.libs import constants
import config.config as pconfig
from avalon_client_sdk.direct.jrpc.worker_registry_jrpc_client import \
    WorkerRegistryJRPCClientImpl
from avalon_client_sdk.direct.jrpc.work_order_jrpc_client import \
    WorkOrderJRPCClientImpl
from avalon_client_sdk.utility.tcf_types import WorkerType
from avalon_client_sdk.direct.jrpc.work_order_receipt_jrpc_client \
     import WorkOrderReceiptJRPCClientImpl
logger = logging.getLogger(__name__)
TCFHOME = os.environ.get("TCF_HOME", "../../")


def submit_request_listener(
        uri_client, input_json_str1, output_json_file_name):
    logger.info("Listener code path\n")
    req_time = time.strftime("%Y%m%d_%H%M%S")
    input_json_str = json.dumps(input_json_str1)
    # write request to file
    signed_input_file = ('./results/' + output_json_file_name + '_' + req_time
                         + '_request.json')
    with open(signed_input_file, 'w') as req_file:
        req_file.write(json.dumps(input_json_str, ensure_ascii=False))
        # json.dump(input_json_str1, req_file)

    logger.info('**********Received Request*********\n%s\n', input_json_str)
    # submit request and retrieve response
    response = uri_client._postmsg(input_json_str)
    logger.info('**********Received Response*********\n%s\n', response)

    # write response to file
    response_output_file = ('./results/' + output_json_file_name + '_'
                            + req_time + '_response.json')
    with open(response_output_file, 'w') as resp_file:
        resp_file.write(json.dumps(response, ensure_ascii=False))

    return response


def submit_work_order_sdk(wo_params, input_json_obj):
    logger.info("SDK code path\n")
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

    return response


def submit_lookup_sdk(worker_type, input_json):
    logger.info("SDK code path\n")
    jrpc_req_id = input_json["id"]
    config = pconfig.parse_configuration_files(
        constants.conffiles, constants.confpaths)
    worker_dict = {'SGX': WorkerType.TEE_SGX,
                   'MPC': WorkerType.MPC, 'ZK': WorkerType.ZK}
    worker_registry = WorkerRegistryJRPCClientImpl(config)

    worker_lookup_response = worker_registry.worker_lookup(
        worker_type=worker_dict[worker_type], id=jrpc_req_id
    )
    logger.info("\n Worker lookup response: {}\n".format(
        json.dumps(worker_lookup_response, indent=4)
    ))

    return worker_lookup_response


def submit_retrieve_sdk(worker_id, input_json):
    logger.info("SDK code path\n")
    jrpc_req_id = input_json["id"]
    config = pconfig.parse_configuration_files(
        constants.conffiles, constants.confpaths)
    worker_registry = WorkerRegistryJRPCClientImpl(config)
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


def submit_create_receipt_sdk(wo_create_receipt, input_json):
    logger.info("SDK code path\n")
    jrpc_req_id = input_json["id"]
    config = pconfig.parse_configuration_files(
        constants.conffiles, constants.confpaths)
    # Create receipt
    wo_receipt = WorkOrderReceiptJRPCClientImpl(config)
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
    return wo_receipt_resp
