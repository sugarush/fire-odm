---
title: 'Load'
date: 2020-02-01T22:42:05-05:00
weight: 8
---

## Load

Loads a record from the database, by its ID.

```python
from fire_odm import MemoryModel

class Data(MemoryModel):
  pass

alpha = await Data.add({ })

beta = Data()
beta.id = alpha.id

await beta.load()
```
