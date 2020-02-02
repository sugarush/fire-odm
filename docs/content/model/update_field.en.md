---
title: 'Update Field'
date: 2020-02-01T19:28:57-05:00
weight: 5
---

A model can be updated with a dictionary or keyword arguments, as so:

```python
from fire_odm import MemoryModel, Field

class Data(MemoryModel):
  field = Field()

# Set data.field to 'one'
data = Data({ 'field': 'one' })

# Set data.field to 'two'
data.update({ 'field': 'two'})

# Set data.field to 'three'
data.update(field='three')
```
