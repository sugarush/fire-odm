from datetime import datetime

from sanic_jsonapi import MongoDBModel, Field

class Name(MongoDBModel):
    first = Field(required=True)
    last = Field(required=True)

class User(MongoDBModel):
    name = Field(type=Name)
    updated = Field(computed='timestamp')
    created = Field(computed='timestamp', computed_empty=True)

    def timestamp(self):
        return datetime.utcnow().timestamp()
