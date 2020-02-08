---
title: 'Exists'
date: 2020-02-01T22:39:29-05:00
weight: 4
---

## Exists

Determines if ID is in the database.

```python
from sugar_odm import MemoryModel

class Data(MemoryModel):
  pass

data = await Data.add({ })

await Data.exists(data.id) # True
```
