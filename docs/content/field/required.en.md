---
title: 'Required'
date: 2019-02-14T14:02:28-05:00
weight: 10
---

```python
from sugar_odm import MemoryModel, Field

class Data(MemoryModel):
  name = Field(required=True)

data = Data()

data.validate() # Raises an Exception

data.name = 'Alice'

data.validate() # Returns None
```
