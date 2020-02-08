---
title: 'Undefined Field'
date: 2020-02-01T22:05:35-05:00
weight: 15
---

IF you try to set a field on a model which has not been defined, you will receive an exception.

```python
from sugar_odm import MemoryModel

class Data(MemoryModel):
  pass

data = Data()

data.set('field', 'test') # Raises an exception.
```
