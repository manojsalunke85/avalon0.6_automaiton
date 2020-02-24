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
import config.config as pconfig
from avalon_client_sdk.direct.jrpc.worker_registry_jrpc_client import \
    WorkerRegistryJRPCClientImpl


logger = logging.getLogger(__name__)


class WorkerLookUp():
    def __init__(self):
        self.id_obj = {"jsonrpc": "2.0", "method": "WorkerLookUp", "id": 1}
        self.params_obj = {}
        self.request_mode = "file"
        self.tamper = {"params": {}}
        self.output_json_file_name = "worker_lookup"

    def add_json_values(self, input_json_temp, tamper):

        if "workerType" in input_json_temp["params"].keys():
            if input_json_temp["params"]["workerType"] != "":
                self.set_worker_type(input_json_temp["params"]["workerType"])
            else:
                self.set_worker_type(1)

        if "id" in input_json_temp.keys():
            self.set_request_id(input_json_temp["id"])

        for key in tamper["params"].keys():
            param = key
            value = tamper["params"][key]
            self.set_unknown_parameter(param, value)

    def set_unknown_parameter(self, param, value):
        self.params_obj[param] = value

    def set_worker_type(self, worker_type):
        self.params_obj["workerType"] = worker_type

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
        if input_json is None:
            self.set_worker_type(1)
        else:
            self.add_json_values(input_json, self.tamper)
        final_json = json.loads(self.to_string())
        return final_json

    def configure_data_sdk(
            self, input_json, worker_obj, pre_test_response):

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
                else:
                    worker_type = worker_value
            except LookupError:
                worker_type = ""

        return worker_type
