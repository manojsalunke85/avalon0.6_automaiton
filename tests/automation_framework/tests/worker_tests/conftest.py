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
import os
import sys
sys.path.append(os.getcwd())
import json
import logging
import config.config as pconfig
from avalon_client_sdk.http_client.http_jrpc_client \
        import HttpJrpcClient
import utility.logger as plogger
from src.libs import constants
from src.utilities.submit_request_utility import \
    submit_request
from src.worker_lookup.worker_lookup_params \
    import WorkerLookUp
from src.worker_retrieve.worker_retrieve_params \
    import WorkerRetrieve
import avalon_client_sdk.worker.worker_details as worker
import crypto_utils.crypto_utility as crypto_utils

TCFHOME = os.environ.get("TCF_HOME", "../../")
logger = logging.getLogger(__name__)
sys.path.append(os.getcwd())


@pytest.fixture(scope="session", autouse=True)
def setup_config(args=None):
    """ Fixture to setup initial config for pytest session. """
    if constants.direct_test_mode == "listener":
        # parse out the configuration file first
        conffiles = ["tcs_config.toml"]
        confpaths = [".", TCFHOME + "/config"]
    
        try:
            config = pconfig.parse_configuration_files(conffiles, confpaths)
            config_json_str = json.dumps(config, indent=4)
        except pconfig.ConfigurationException as e:
            logger.error(str(e))
            sys.exit(-1)
    
        plogger.setup_loggers(config.get("Logging", {}))
        sys.stdout = plogger.stream_to_logger((logging.getLogger("STDOUT"),
                                               logging.DEBUG))
        sys.stderr = plogger.stream_to_logger((logging.getLogger("STDERR"),
                                               logging.WARN))
    
        logger.info("configuration for the session: %s", config)
    
        uri_client_str = config['tcf']['json_rpc_uri']
        logger.info("URI Client string %s", uri_client_str)
    
        uri_client = HttpJrpcClient(uri_client_str)

        return uri_client
