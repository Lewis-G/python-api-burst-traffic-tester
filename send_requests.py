import requests
import concurrent.futures
import time
import json
import os

def create_request_args(config:dict):
    
    request_args = {
        "method": config["method"],
        "url": config["url"],
        "headers": config["headers"],
        "params": config["params"]
    }

    # Add 'json' argument only if the method is not GET
    if config["method"].upper() != "GET" and "body" in config:
        request_args["json"] = config["body"]
    
    # Add 'params' only if config.json 'parameters' is not empty
    params = config.get("params", {})
    if params:
        request_args["params"] = params

def send_request(config:dict):
    response = None
    try:
        response = requests.request(method=config["method"], url=config["url"], headers=config["headers"], params=config["params"], json=config["body"])    
    except Exception as e:
        print(f"Request failed: {e}")
        
    try:
        print(f"Status Code: {response.status_code}, Response Time: {response.elapsed.total_seconds()}s")
        print(f"Response text: {response.text}\n")
    except Exception as e:
        print(f"Parsing response failed: {e}")
        
def concurrent_requests(request_data, is_array=False):
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=request_data["numberOfRequests"]) as executor:

        futures_list = []
        for i in range(request_data["numberOfRequests"]):
            
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
    
    request_args = create_request_args(config)
    
    concurrent_requests(request_args)