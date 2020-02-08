---
title: 'Missing Field'
date: 2020-02-01T22:05:40-05:00
weight: 10
---

If a field is marked as required, and is missing when validated/saved, an exception will be raised.

```python
from sugar_odm import MemoryModel, Field

class Data(MemoryModel):
  field = Field(required=True)

data = Data()

data.validate() # Raises an exception.
```
