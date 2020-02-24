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
import avalon_client_sdk.worker.worker_details as worker
import crypto_utils.crypto_utility as crypto_utils
logger = logging.getLogger(__name__)


class WorkerRetrieve():
    def __init__(self):
        self.id_obj = {"jsonrpc": "2.0", "method": "WorkerRetrieve", "id": 2}
        self.params_obj = {}
        self.request_mode = "file"
        self.tamper = {"params": {}}
        self.output_json_file_name = "worker_retrieve"

    def add_json_values(self, input_json_temp, worker_obj, tamper):

        if "workerId" in input_json_temp["params"].keys():
            if input_json_temp["params"]["workerId"] != "":
                self.set_worker_id(input_json_temp["params"]["workerId"])
            else:
                worker_id = worker_obj.worker_id
                self.set_worker_id(worker_id)

        if "id" in input_json_temp.keys():
            self.set_request_id(input_json_temp["id"])

        for key in tamper["params"].keys():
            param = key
            value = tamper["params"][key]
            self.set_unknown_parameter(param, value)

    def set_unknown_parameter(self, param, value):
        self.params_obj[param] = value

    def set_worker_id(self, worker_id):
        self.params_obj["workerId"] = worker_id

    def set_request_id(self, request_id):
        self.id_obj["id"] = request_id

    def get_params(self):
        return self.params_obj.copy()

    def to_string(self):
        json_rpc_request = self.id_obj
        json_rpc_request["params"] = self.get_params()

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

        return worker_id
