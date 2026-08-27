
import json

with open("results.json") as f:
    data = json.load(f)

assert "model" in data
assert "gpu" in data
assert "measurements" in data

assert len(data["measurements"]) == 3

types = [x["dtype"] for x in data["measurements"]]

assert "fp16" in types
assert "int8" in types
assert "int4" in types

print("GREEN CHECK: PASS")
