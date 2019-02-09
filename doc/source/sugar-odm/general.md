# General

Sugar ODM is an asynchronous Object-Document Mapper written in Python. It supports *nested models*, *validation* and *computed fields*. It currently boasts __memory__ and __MongoDB__ backends.


The following is a basic example of using *nested models* with the __memory__ backend.
```
import asyncio

from sugar_odm import MemoryModel, Model, Field


class Name(Model):
  first = Field(required=True)
  last = Field(required=True)


class User(MemoryModel):
  name = Field(type=Name)


async def main():

  user = User({ 'name': { 'first': 'Alice', 'last': 'Jane' } })
  await user.save()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```
