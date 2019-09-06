---
title: 'Computed'
date: 2019-02-14T14:01:57-05:00
weight: 20
---

A field can be a computed property.

```python
class Data(MemoryModel):
  first = Field(required=True)
  last = Field(required=True)
  full = Field(computed='full_name')

  def full_name(self):
    return f'{self.first} {self.last}'
```
