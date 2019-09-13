import json, re
from datetime import datetime

def serialize(dict):
    return json.dumps(dict, separators=(',', ':'), sort_keys=True)

def inject_query(*args):
    if len(args) == 1:
        _inject(args[0])

def _inject(query):
    for (key, value) in query.items():
        if isinstance(value, dict):
            _inject(query[key])
        elif isinstance(value, str):
            match = re.fullmatch('Date\((?P<date>.*)\)', value)
            if match:
                query[key] = datetime.fromisoformat(match.groupdict()['date'])
