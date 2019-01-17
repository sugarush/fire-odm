from datetime import datetime

from sugar_odm import MongoDBModel, Field


class Type(MongoDBModel):
    name = Field(required=True)

class Name(MongoDBModel):
    first = Field(required=True)
    last = Field(required=True)

class User(MongoDBModel):
    name = Field(type=Name)
    type = Field(required=True)
    updated = Field(computed='timestamp')
    created = Field(computed='timestamp', computed_empty=True)

    def timestamp(self):
        return datetime.utcnow().timestamp()
