from collections import defaultdict
import time

request_count = defaultdict(int)
request_latency = defaultdict(list)
error_count = defaultdict(int)

def record_request(path:str ,duration:float, success:bool):
    request_count[path] += 1
    request_latency[path].append(duration)
    if not success:
        error_count += 1