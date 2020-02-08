---
title: 'Memory'
date: 2020-02-01T20:20:54-05:00
weight: 5
---

The **MemoryModel** query system relies on simple key matching.

## Example

```python
from sugar_odm import MemoryModel, Field

class Data(MemoryModel):
  field = Field()

await Data.add([
  { 'field': 'one' },
  { 'field': 'two' }
])

async for data in Data.find({ 'field': 'one' }):
  print(data)
```
