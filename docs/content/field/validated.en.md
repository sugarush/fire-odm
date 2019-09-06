---
title: 'Validated'
date: 2019-02-14T14:02:03-05:00
weight: 15
---

A field can be validated with an instance method.

```python
class Data(MemoryModel):
  name = Field(validated='validate_name')

  def validate_name(self, value):
    if not len(value) < 10:
      raise Exception(f'Field "name" length greater than 10.')

data = Data({ 'name': 'testing123' })

data.validate() # Raises an exception.
```
