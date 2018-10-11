import json

def serialize(dict):
    return json.dumps(dict, separators=(',', ':'), sort_keys=True)
