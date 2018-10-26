from datetime import datetime

import rethinkdb as r

from sanic_jsonapi import RethinkDBModel, Field

class Name(RethinkDBModel):
    first = Field(required=True)
    last = Field(required=True)

class User(RethinkDBModel):
    #id = Field(type=int, primary=True)
    name = Field(type=Name)
    updated = Field(type='set_timestamp', computed='timestamp')
    created = Field(type='set_timestamp', computed='timestamp', computed_empty=True)

    def timestamp(self):
        return r.now()

    def set_timestamp(self, value):
        if isinstance(value, datetime):
            return value.isoformat()
        return value
