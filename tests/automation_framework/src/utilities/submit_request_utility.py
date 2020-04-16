import logging
import json
import time
import os
import sys
from src.libs import constants
import config.config as pconfig
import globals
from avalon_sdk.direct.jrpc.jrpc_worker_registry import \
    JRPCWorkerRegistryImpl
from avalon_sdk.direct.jrpc.jrpc_work_order import \
    JRPCWorkOrderImpl
from avalon_sdk.worker.worker_details import \
    WorkerType, WorkerStatus
from avalon_sdk.direct.jrpc.jrpc_work_order_receipt \
    import JRPCWorkOrderReceiptImpl
from avalon_sdk.fabric.fabric_worker_registry \
    import FabricWorkerRegistryImpl
from avalon_sdk.fabric.fabric_work_order \
    import FabricWorkOrderImpl
from src.utilities.generic_utils import GetResultWaitTime
from avalon_sdk.ethereum.ethereum_worker_registry \
    import EthereumWorkerRegistryImpl
from avalon_sdk.ethereum.ethereum_work_order \
    import EthereumWorkOrderProxyImpl
from avalon_sdk.ethereum.ethereum_wrapper \
    import EthereumWrapper
import avalon_sdk.worker.worker_details as worker_details
logger = logging.getLogger(__name__)
TCFHOME = os.environ.get("TCF_HOME", "../../")


def _create_worker_registry_instance(blockchain_type, config):
    # create worker registry instance for direct/proxy model
    if constants.proxy_mode and blockchain_type == 'fabric':
        return FabricWorkerRegistryImpl(config)
    elif constants.proxy_mode and blockchain_type == 'ethereum':
        return EthereumWorkerRegistryImpl(config)
    else:
        logger.info("Direct SDK code path\n")
        return JRPCWorkerRegistryImpl(config)


def _create_work_order_instance(blockchain_type, config):
    # create work order instance for direct/proxy model
    if constants.proxy_mode and blockchain_type == 'fabric':
        return FabricWorkOrderImpl(config)
    elif constants.proxy_mode and blockchain_type == 'ethereum':
        return EthereumWorkOrderProxyImpl(config)
    else:
        logger.info("Direct SDK code path\n")
        return JRPCWorkOrderImpl(config)


def _create_work_order_receipt_instance(blockchain_type, config):
    # create work order receipt instance for direct/proxy model
    if constants.proxy_mode and blockchain_type == 'fabric':
        return None
    elif constants.proxy_mode and blockchain_type == 'ethereum':
        # TODO need to implement
        return None
    else:
        logger.info("Direct SDK code path\n")
        return JRPCWorkOrderReceiptImpl(config)


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

    logger.info('**********Received Request*********\n%s\n', input_json_str)
    response = uri_client._postmsg(input_json_str)
    logger.info('**********Received Response*********\n%s\n', response)

    # write response to file
    response_output_file = ('./results/' + output_json_file_name + '_'
                            + req_time + '_response.json')
    with open(response_output_file, 'w') as resp_file:
        resp_file.write(json.dumps(response, ensure_ascii=False))

    return response


def submit_work_order_sdk(wo_params, input_json_obj=None):
    logger.info("SDK code path\n")
    if input_json_obj is None:
        req_id = 3
    else:
        req_id = input_json_obj["id"]
    config = pconfig.parse_configuration_files(
        constants.conffiles, constants.confpaths)
    logger.info(" URI client %s \n", config["tcf"]["json_rpc_uri"])

    work_order = _create_work_order_instance(globals.blockchain_type, config)
    logger.info(" work order id %s \n", wo_params.get_work_order_id())
    logger.info(" worker id %s \n", wo_params.get_worker_id())
    logger.info(" Requester ID %s \n", wo_params.get_requester_id())
    logger.info(" To string %s \n", wo_params.to_string())

    logger.info(" worker id %s \n", wo_params.get_worker_id())
    logger.info("Work order submit request : %s, \n \n ",
                wo_params.to_jrpc_string(req_id))
    response = work_order.work_order_submit(
        wo_params.get_work_order_id(),
        wo_params.get_worker_id(),
        wo_params.get_requester_id(),
        wo_params.to_string(),
        id=req_id
    )

    return response


def submit_lookup_sdk(worker_type, input_json=None):
    logger.info("SDK code path\n")
    if input_json is None:
        jrpc_req_id = 3
    else:
        jrpc_req_id = input_json["id"]
    config = pconfig.parse_configuration_files(
        constants.conffiles, constants.confpaths)
    logger.info(" URI client %s \n", config["tcf"]["json_rpc_uri"])
    worker_dict = {'SGX': WorkerType.TEE_SGX,
                   'MPC': WorkerType.MPC, 'ZK': WorkerType.ZK}
    worker_registry = _create_worker_registry_instance(globals.blockchain_type, config)
    if globals.blockchain_type == "ethereum":
        worker_lookup_response = worker_registry.worker_lookup(
            WorkerType.TEE_SGX,
            config["WorkerConfig"]["OrganizationId"],
            config["WorkerConfig"]["ApplicationTypeId"],
            jrpc_req_id
        )
    else:
        worker_lookup_response = worker_registry.worker_lookup(
        worker_type=worker_dict[worker_type], id=jrpc_req_id)
    logger.info("\n Worker lookup response: {}\n".format(
        json.dumps(worker_lookup_response, indent=4)
    ))

    return worker_lookup_response


def submit_register_sdk(dummy, input_json):
    logger.info("SDK code path\n")
    jrpc_req_id = input_json["id"]
    config = pconfig.parse_configuration_files(
        constants.conffiles, constants.confpaths)
    logger.info(" URI client %s \n", config["tcf"]["json_rpc_uri"])
    worker_registry = _create_worker_registry_instance(globals.blockchain_type, config)
    worker_register_result = worker_registry.worker_register(
        input_json["params"]["workerId"], input_json["params"]["workerType"],
        input_json["params"]["organizationId"],
        input_json["params"]["applicationTypeId"],
        input_json["params"]["details"])
    logger.info("\n Worker register response: {}\n".format(
        json.dumps(worker_register_result, indent=4)))
    return worker_register_result


def submit_setstatus_sdk(dummy, input_json):
    logger.info("SDK code path\n")
    jrpc_req_id = input_json["id"]
    status_dict = {1: WorkerStatus.ACTIVE, 2: WorkerStatus.OFF_LINE,
                   3: WorkerStatus.DECOMMISSIONED,
                   4: WorkerStatus.COMPROMISED}
    config = pconfig.parse_configuration_files(
        constants.conffiles, constants.confpaths)
    logger.info(" URI client %s \n", config["tcf"]["json_rpc_uri"])
    worker_registry = _create_worker_registry_instance(globals.blockchain_type, config)
    worker_setstatus_result = worker_registry.worker_set_status(
        input_json["params"]["workerId"],
        status_dict[input_json["params"]["status"]])
    logger.info("\n Worker setstatus response: {}\n".format(
        json.dumps(worker_setstatus_result, indent=4)))
    return worker_setstatus_result


def submit_retrieve_sdk(worker_id, input_json=None):
    logger.info("SDK code path\n")
    worker_obj = worker_details.SGXWorkerDetails()
    if input_json is None:
        jrpc_req_id = 11
    else:
        jrpc_req_id = input_json["id"]
    config = pconfig.parse_configuration_files(
        constants.conffiles, constants.confpaths)
    logger.info(" URI client %s \n", config["tcf"]["json_rpc_uri"])
    worker_registry = _create_worker_registry_instance(globals.blockchain_type, config)
    if constants.proxy_mode and globals.blockchain_type == 'ethereum':
        for w_id in worker_id:
            worker = worker_registry\
                .worker_retrieve(w_id, jrpc_req_id)
            if worker["result"]["status"] == \
                WorkerStatus.ACTIVE.value:
                worker_retrieve_result = worker
                worker_id = w_id
                break
        logger.info("\n Worker ID\n%s\n", worker_id)
        logger.info("\n Worker retrieve response: {}\n".format(
            json.dumps(worker_retrieve_result, indent=4)))
    else:
        worker_retrieve_result = worker_registry.worker_retrieve(
            worker_id, jrpc_req_id)
        logger.info("\n Worker retrieve response: {}\n".format(
            json.dumps(worker_retrieve_result, indent=4)))

        if "error" in worker_retrieve_result:
            logger.error("Unable to retrieve worker details\n")
            sys.exit(1)
    if constants.proxy_mode and globals.blockchain_type == 'fabric':
        worker_obj.load_worker(json.loads(worker_retrieve_result[4]))
    else:
        worker_obj.load_worker(worker_retrieve_result['result']['details'])
    worker_obj.worker_id = worker_id
    logger.info("\n Worker ID\n%s\n", worker_obj.worker_id)
    if input_json is None:
        return worker_obj
    else:
        return worker_retrieve_result


def submit_update_sdk(update_params, input_json=None):
    logger.info("SDK code path\n")
    logger.info("Worker update params %s \n", update_params)
    worker_obj = worker_details.SGXWorkerDetails()
    # update_params = json.loads(update_params)
    if input_json is None:
        jrpc_req_id = 11
    else:
        jrpc_req_id = input_json["id"]
    config = pconfig.parse_configuration_files(
        constants.conffiles, constants.confpaths)
    logger.info(" URI client %s \n", config["tcf"]["json_rpc_uri"])
    worker_registry = _create_worker_registry_instance(globals.blockchain_type, config)
    if not constants.proxy_mode:
        worker_update_result = worker_registry.worker_update(
            eval(str(update_params))["worker_id"],
            eval(str(update_params))["details"], jrpc_req_id)
        logger.info("\n Worker update response: {}\n".format(
            json.dumps(worker_update_result, indent=4)))

    return worker_update_result

def submit_create_receipt_sdk(wo_create_receipt, input_json):
    logger.info("SDK code path\n")
    jrpc_req_id = input_json["id"]
    config = pconfig.parse_configuration_files(
        constants.conffiles, constants.confpaths)
    logger.info(" URI client %s \n", config["tcf"]["json_rpc_uri"])
    # Create receipt
    wo_receipt = _create_work_order_receipt_instance(globals.blockchain_type, config)
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

def submit_retrieve_receipt_sdk(workorderId, input_json):
    logger.info("SDK code path\n")
    jrpc_req_id = input_json["id"]
    config = pconfig.parse_configuration_files(
        constants.conffiles, constants.confpaths)
    logger.info(" URI client %s \n", config["tcf"]["json_rpc_uri"])
    # Create receipt
    wo_receipt = _create_work_order_receipt_instance(globals.blockchain_type, config)

    wo_receipt_resp = wo_receipt.work_order_receipt_retrieve(
        workorderId, jrpc_req_id)

    logger.info("Work order retrieve receipt response : {} \n \n ".format(
        wo_receipt_resp
    ))
    return wo_receipt_resp

def submit_getresult_sdk(workorderId, input_json):
    logger.info("SDK code path\n")
    jrpc_req_id = input_json["id"]
    config = pconfig.parse_configuration_files(
        constants.conffiles, constants.confpaths)

    logger.info(" URI client %s \n", config["tcf"]["json_rpc_uri"])

    work_order = _create_work_order_instance(globals.blockchain_type, config)
    logger.info("----- Validating WorkOrderGetResult Response ------")


    get_result_res = work_order.work_order_get_result(
        workorderId, jrpc_req_id)
    logger.info("******Received Response*****\n%s\n", get_result_res)

    return get_result_res
