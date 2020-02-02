---
title: 'Find'
date: 2020-02-01T22:37:11-05:00
weight: 1
---

## Find

Finds models by query.

```python
from fire_odm import MemoryModel, Field

class Data(MemoryModel):
  field = Field()

await Data.add({ 'field': 'value' })

async for data in Data.find({ 'field': 'value' }):
  print(data)
```
