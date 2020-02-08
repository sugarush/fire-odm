---
title: 'Save'
date: 2020-02-01T22:42:02-05:00
weight: 7
---

## Save

Saves a record to the database.

```python
from sugar_odm import MemoryModel, Field

class Data(MemoryModel):
  field = Field()

data = Data({ 'field': 'value' })

await data.save()
```
