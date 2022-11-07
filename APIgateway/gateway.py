from fastapi import FastAPI

app = FastAPI()

registered_ports = [8000, 8001, 8002, 8003, 8004, 8005, 8006, 8007, 8008]
service_list = []
for port in registered_ports:
    for service in requests.get("http://localhost:"+port):
        service_list.append(service)