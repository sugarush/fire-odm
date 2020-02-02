---
title: 'Validated'
date: 2019-02-14T14:02:03-05:00
weight: 15
---

A field can be validated with an instance method.

```python
from fire_odm import MemoryModel, Field

class Data(MemoryModel):
  name = Field(validated='validate_name')

  def validate_name(self, value):
    if len(value) > 5:
      raise Exception(f'Field "name" length greater than 5.')

data = Data({ 'name': 'testing' }) # Raises an exception.
```
