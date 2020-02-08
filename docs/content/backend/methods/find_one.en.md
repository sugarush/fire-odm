---
title: 'Find One'
date: 2020-02-01T22:39:25-05:00
weight: 3
---

## Find One

Returns the first model matching the query.

```python
from sugar_odm import MemoryModel, Field

class Data(MemoryModel):
  field = Field()

await Data.add([
  { 'field': 'value' },
  { 'field': 'value' }
])

data = await Data.find_one({ 'field': 'value' })

data.field == 'value' # True
```
