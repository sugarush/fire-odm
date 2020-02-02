---
title: 'Count'
date: 2020-02-01T22:39:33-05:00
weight: 5
---

## Count

Returns the number of records in the table/collection.

```python
from fire_odm import MemoryModel, Field

class Data(MemoryModel):
  field = Field()

await Data.add([
  { 'field': 'value' },
  { 'field': 'value' }
])

await Data.count() # 2
```
