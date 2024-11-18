import requests
import concurrent.futures
import time
import json
import os
from typing import Union
import copy


def create_request_args(config: dict):

    request_args = {
        "method": config["method"],
        "url": config["url"],
        "headers": config["headers"]
    }

    # Add 'json' argument only if the method is not GET, and if 'body' in config.json is not empty
    json = config.get("body", {})
    if config["method"].upper() != "GET" and json:
        request_args["json"] = json

    # Add 'params' only if 'parameters' in config.json is not empty
    params = config.get("params", {})
    if params:
        request_args["params"] = params

    return request_args


def create_request_args_list(request_args: dict, request_num: int):

    request_args_list = []

    for i in range(request_num):
        temp_request_args = copy.deepcopy(request_args)

        # Enter in your custom logic here, to create unqiue requests
        # For example, you want to execute a request using differing route params:
        # .../api/people/1 , ...api/people/2, .../api/people/3

        # Examples
        # temp_request_args["params"]["id"] == {i}
        # temp_request_args["body"]["org name"] == f"Org number {i}"

        temp_request_args["params"]["q"] = f"YouTube Data API tutorials - Part {i}"

        request_args_list.append(temp_request_args)

    return request_args_list


def send_request(request_args: dict):

    response = None
    try:
        response = requests.request(**request_args)
    except Exception as e:
        print(f"Request failed: {e}")

    try:
        print(f"Status Code: {response.status_code}, Response Time: {
              response.elapsed.total_seconds()}s")
        print(f"Response text: {response.text}\n")
    except Exception as e:
        print(f"Parsing response failed: {e}")


def concurrent_requests(request_data: Union[dict, list], request_num: int, is_array=False):
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=request_num) as executor:

        futures_list = []
        for i in range(request_num):

            if (is_array == False):
                future = executor.submit(send_request, request_data)
            else:
                future = executor.submit(send_request, request_data[i])

            futures_list.append(future)

        concurrent.futures.wait(futures_list)

    end_time = time.time()
    print(f"Total time taken: {end_time - start_time}s")


if __name__ == "__main__":

    config_path = os.path.join(os.getcwd(), 'config.json')

    with open(config_path, "r") as file:
        config = json.load(file)

    request_num = config["numberOfRequests"]

    request_args = create_request_args(config)

    concurrent_requests(request_args, request_num)

    # To create a list of request args
    # Comment out the line above, and uncomment the two lines below

    # request_args_list = create_request_args_list(request_args, request_num)
    # concurrent_requests(request_args_list, request_num, True)
