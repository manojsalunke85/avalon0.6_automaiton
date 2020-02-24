import pytest
import time
import os
import sys
import argparse
import json
import logging
import config.config as pconfig
from avalon_client_sdk.http_client.http_jrpc_client \
        import HttpJrpcClient
import utility.logger as plogger
TCFHOME = os.environ.get("TCF_HOME", "../../")
logger = logging.getLogger(__name__)
sys.path.append(os.getcwd())


@pytest.fixture(scope="session", autouse=True)
def setup_config(args=None):
    """ Fixture to setup initial config for pytest session. """

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
