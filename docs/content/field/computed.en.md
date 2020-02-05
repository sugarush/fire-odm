---
title: 'Computed'
date: 2019-02-14T14:01:57-05:00
weight: 20
---

A field can be a computed property.

{{% notice info %}}
A computed property is only generated when the model is serialized, which happens at save time and when the model is printed.
{{% /notice %}}

```python
from fire_odm import MemoryModel, Field

class Data(MemoryModel):
  first = Field(required=True)
  last = Field(required=True)
  full = Field(computed='full_name')

  def full_name(self):
    return f'{self.first} {self.last}'

data = Data({ 'first': 'Alice', 'last': 'Jane' })

await data.save()

data.full # Prints 'Alice Jane'
```
