---
title: 'Interpreter'
date: 2019-02-09T19:01:15-05:00
weight: 10
---

Fire ODM can be used with the IPython interpreter.

```shell
pip install ipython
```

From the IPython interpreter one can easily create, read, update and delete records:
```python
from fire_odm import MemoryModel, Model, Field

class Name(Model):
  first = Field(required=True)
  last = Field(required=True)

class User(MemoryModel):
  name = Field(type=Name)

user = User({ 'name': { 'first': 'Alice', 'last': 'Jane' } })

await user.save()

async for user in User.find():
  print(user)
```
