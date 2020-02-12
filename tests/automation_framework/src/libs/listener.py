from src.worker_lookup.worker_lookup_params \
    import WorkerLookUp
from src.worker_retrieve.worker_retrieve_params \
    import WorkerRetrieve
import avalon_client_sdk.worker.worker_details as worker
from avalon_client_sdk.utility.tcf_types import WorkerType
import crypto_utils.crypto_utility as crypto_utils
import logging
import json
from src.libs import constants
from src.utilities.submit_request_utility import \
    submit_request

logger = logging.getLogger(__name__)


def worker_lookup_listener(uri_client, input_json=None):

    """ Function for computing worker lookup and retrieve once per session. """

    if not uri_client:
        logger.error("Server URI is not provided")
        exit(1)

    lookup_obj = WorkerLookUp()
    if input_json is None:
        worker_type = 1
    else:
        try:
            worker_type = input_json["params"]["workerType"]
            lookup_obj.set_worker_type(worker_type)
        except LookupError:
            logger.info("No params for worker type specified")

    input_worker_look_up = json.loads(lookup_obj.to_string())

    # input_json_str = input_worker_look_up
    logger.info("------------------Testing WorkerLookUp------------------")

    # submit worker lookup request and retrieve response
    logger.info("********Received Request*******\n%s\n", input_worker_look_up)
    response = submit_request(uri_client, input_worker_look_up,
                              constants.worker_lookup_output_json_file_name)
    logger.info("**********Received Response*********\n%s\n", response)

    return response


def worker_retrieve_listener(lookup_response, uri_client):

    err_cd = 0
    logger.info("-----Testing WorkerRetrieve-----")
    # Retrieving the worker id from the "WorkerLookUp" response and
    # update the worker id information for the further json requests

    worker_obj = worker.SGXWorkerDetails()

    retrieve_obj = WorkerRetrieve()

    if "result" in lookup_response and "ids" \
            in lookup_response["result"].keys():
        retrieve_obj.set_worker_id(crypto_utils.strip_begin_end_public_key
                                   (lookup_response["result"]["ids"][0]))
        input_worker_retrieve = json.loads(retrieve_obj.to_string())
        logger.info('*****Worker details Updated with Worker ID***** \
                       \n%s\n', input_worker_retrieve)
    else:
        logger.info('ERROR: Failed at WorkerLookUp - \
                   No Worker ids in WorkerLookUp response.')
        err_cd = 1

    if err_cd == 0:
        # submit worker retrieve request and load to worker object
        retrieve_response = submit_request(
            uri_client, input_worker_retrieve,
            constants.worker_retrieve_output_json_file_name)
        worker_obj.load_worker(retrieve_response)

    return worker_obj, err_cd, retrieve_response
