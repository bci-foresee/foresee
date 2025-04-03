import requests
import json

with open("dev_tests/shiao_pipeline.json") as f:
    data = json.load(f)

res = requests.post("http://127.0.0.1:5000/run-pipeline", json=data)
print(res.status_code)
print(res.json())
