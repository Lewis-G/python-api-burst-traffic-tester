import requests
import concurrent.futures
import time
import json
import os

def send_request(config:dict):
    response = None
    try:
        # Make the request with the specified HTTP method
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
    
    # # Create an array, modify body values, so that each request is different
    # request_data = []
    # for i in range(config["numberOfRequests"]):
    #     request_data.append(config)
    #     request_data[i]["body"]["org name"] == f"Org number {i}"
    
    concurrent_requests(config)