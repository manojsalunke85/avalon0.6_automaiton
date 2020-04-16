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

import json
import logging
from src.libs import constants
import globals
import avalon_sdk.worker.worker_details as worker
import avalon_crypto_utils.crypto_utility as crypto_utils

logger = logging.getLogger(__name__)


class WorkerUpdate():
    def __init__(self):
        self.id_obj = {"jsonrpc": "2.0", "method": "WorkerUpdate", "id": 11}
        self.params_obj = {}
        self.details_obj = {}
        self.request_mode = "file"
        self.tamper = {"params": {}}
        self.output_json_file_name = "worker_update"

    def add_json_values(self, input_json_temp, worker_obj, tamper):

        if "workerId" in input_json_temp["params"].keys():
            if input_json_temp["params"]["workerId"] != "":
                self.set_worker_id(input_json_temp["params"]["workerId"])
            else:
                worker_id = worker_obj.worker_id
                self.set_worker_id(worker_id)

        if "id" in input_json_temp.keys():
            self.set_request_id(input_json_temp["id"])

        if "details" in input_json_temp["params"].keys():
            if ("hashingAlgorithm" in
                    input_json_temp["params"]["details"].keys()):
                if input_json_temp["params"]["details"]["hashingAlgorithm"] \
                        != "":
                    self.set_hashing_algorithm(
                        input_json_temp["params"]
                        ["details"]["hashingAlgorithm"])
                else:
                    self.set_hashing_algorithm(worker_obj.hashing_algorithm)

            elif ("signingAlgorithm" in
                    input_json_temp["params"]["details"].keys()):
                self.set_signing_algorithm(
                    input_json_temp["params"]["details"]["signingAlgorithm"])

            elif ("keyEncryptionAlgorithm" in
                    input_json_temp["params"]["details"].keys()):
                self.set_key_encryption_algorithm(
                    input_json_temp["params"]
                    ["details"]["keyEncryptionAlgorithm"])

            elif ("dataEncryptionAlgorithm" in
                    input_json_temp["params"]["details"].keys()):
                self.set_data_encryption_algorithm(
                    input_json_temp["params"]
                    ["details"]["dataEncryptionAlgorithm"])
            else:
                for key in \
                        input_json_temp["params"]["details"].keys():
                    param = key
                    value = input_json_temp["params"]["details"][key]
                    self.set_unknown_parameter_detail(param, value)

                ''' for key in input_json_temp["params"].keys():
                    param = key
                    value = tamper["params"][key]
                    self.set_unknown_parameter(param, value)

            if "details" in tamper["params"].keys():
            for key in tamper["params"]["details"].keys():
                detail = key
                value = tamper["params"]["details"][key]
                self.set_unknown_parameter_detail(param, value)'''

    def set_unknown_parameter(self, param, value):
        self.params_obj[param] = value

    def set_unknown_parameter_detail(self, detail, value):
        self.details_obj[detail] = value

    def set_worker_id(self, worker_id):
        self.params_obj["workerId"] = worker_id

    def set_request_id(self, request_id):
        self.id_obj["id"] = request_id

    def set_hashing_algorithm(self, hashing_algorithm):
        self.details_obj["hashingAlgorithm"] = hashing_algorithm

    def set_signing_algorithm(self, signing_algorithm):
        self.details_obj["signingAlgorithm"] = signing_algorithm

    def set_key_encryption_algorithm(self, key_encryption_algorithm):
        self.details_obj["keyEncryptionAlgorithm"] = key_encryption_algorithm

    def set_data_encryption_algorithm(self, data_encryption_algorithm):
        self.details_obj["dataEncryptionAlgorithm"] = data_encryption_algorithm

    def get_params(self):
        return self.params_obj.copy()

    def get_details(self):
        return self.details_obj.copy()

    def to_string(self):
        json_rpc_request = self.id_obj
        json_rpc_request["params"] = self.get_params()
        json_rpc_request["params"]["details"] = self.get_details()

        return json.dumps(json_rpc_request, indent=4)

    def configure_data(
            self, input_json, worker_obj, pre_test_response):
        worker_obj = worker.SGXWorkerDetails()
        if input_json is not None:
            self.add_json_values(
                input_json, worker_obj, self.tamper)
        self.set_worker_id(
            crypto_utils.strip_begin_end_public_key
            (pre_test_response["result"]["ids"][0]))

        input_worker_retrieve = json.loads(self.to_string())
        logger.info('*****Worker details Updated with Worker ID***** \
                           \n%s\n', input_worker_retrieve)
        return input_worker_retrieve

    def configure_data_sdk(
            self, input_json, worker_obj, pre_test_response):
        if constants.proxy_mode and \
            globals.blockchain_type == "ethereum":
            if "result" in pre_test_response and \
                "ids" in pre_test_response["result"].keys():
                if pre_test_response["result"]["totalCount"] != 0:
                    worker_id = pre_test_response["result"]["ids"]
                    # Filter workers by status(active) field
                    # Return first worker whose status is active
                else:
                    logger.error("No workers found")
            else:
                logger.error("Failed to lookup worker")
        elif constants.proxy_mode and \
            globals.blockchain_type == "fabric":
            worker_id = pre_test_response[2][0]
        else:
            if "result" in pre_test_response and \
                "ids" in pre_test_response["result"].keys():
                if pre_test_response["result"]["totalCount"] != 0:
                    worker_id = pre_test_response["result"]["ids"][0]
                else:
                    logger.error("ERROR: No workers found")
                    worker_id = None
            else:
                logger.error("ERROR: Failed to lookup worker")
                worker_id = None
        details = input_json["params"]["details"]

        update_params = {"worker_id": worker_id, "details": details}

        return update_params
