import os

TCFHOME = os.environ.get("TCF_HOME", "../../")

work_order_input_file = os.path.join(os.getcwd(), 'data', 'work_order')

worker_input_file = os.path.join(os.getcwd(), 'data', 'worker')

# expected response
check_submit = {"error": {"code": 5}}

# tamper parameters
wo_submit_tamper = {"params": {}}

# request mode - file, string or object
wo_submit_request_mode = "file"

# output filename
wo_submit_output_json_file_name = 'work_order_success'

wo_result_request_mode = "object"

wo_result_tamper = {}

wo_result_output_json_file_name = "work_order_get_result"

worker_request_mode = "file"

worker_lookup_tamper = {"params": {}}

worker_lookup_output_json_file_name = "worker_lookup"

worker_request_id = 0

worker_retrieve_output_json_file_name = "worker_lookup"

worker_retrieve_tamper = {"params": {}}

# Direct test mode = listener or client_sdk
direct_test_mode = "listener"

# Config file path
conffiles = ["tcs_config.toml"]
confpaths = [".", TCFHOME + "/config"]
