---
title: 'Delete'
date: 2020-02-01T22:42:08-05:00
weight: 9
---

## Delete

Deletes a record from the database.

```python
from fire_odm import MemoryModel

class Data(MemoryModel):
  pass

data = await Data.add({ })

await data.delete()
```
