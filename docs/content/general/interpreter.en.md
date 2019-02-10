---
title: 'Interpreter'
date: 2019-02-09T19:01:15-05:00
weight: 10
---

Sugar ODM can easily be used with the IPython interpreter.

```shell
pip install ipython git+https://github.com/sugarush/sugar-odm@master#egg=sugar-odm

ipython
```

From there, one can create and find records:
```python
from sugar_odm import MemoryModel, Model, Field

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
