---
title: 'Find By ID'
date: 2020-02-01T22:37:17-05:00
weight: 2
---

## Find By ID

Finds a model by its ID.

```python
from sugar_odm import MemoryModel

class Data(MemoryModel):
  pass

alpha = await Data.add({ })

beta = await Data.find_by_id(alpha.id)

alpha.id == beta.id # True
```
