---
title: 'Drop'
date: 2020-02-01T22:42:12-05:00
weight: 10
---

## Drop

Drops a table/collection.

```python
from sugar_odm import MemoryModel

class Data(MemoryModel):
  pass

await Data.add({ })

await Data.drop()

await Data.count() # 0
```
