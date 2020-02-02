---
title: 'Add'
date: 2020-02-01T22:41:59-05:00
weight: 6
---

## Add

Adds a model or models to the database and returns it/them.

Single-model example.

```python
from fire_odm import MemoryModel, Field

class Data(MemoryModel):
  field = Field()

await Data.add({ 'field': 'one' })
```

Multi-model example.

```python
from fire_odm import MemoryModel, Field

class Data(MemoryModel):
  field = Field()

await Data.add([
  { 'field': 'two' },
  { 'field': 'three' }
])
```
