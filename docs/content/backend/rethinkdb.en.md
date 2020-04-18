---
title: 'RethinkDB'
date: 2020-04-18T15:59:55-04:00
weight: 15
---

## Example

Find all records in a table.

```python
from sugar_odm import RethinkDBModel, Field

class Model(RethinkDBModel):

  __connection__ = {
    'host': 'localhost',
    'port': 28015,
    'user': 'admin',
    'password': '',
    'timeout': 20,
    'ssl': {
      'ca_certs': '/path/to/ca.crt'
    }
  }

  __database__ = {
    'name': 'test'
  }

  field = Field()

await Model.add([
  { 'field': 'alpha' },
  { 'field': 'beta' }
])

[ model async for model in Model.find() ]
```
