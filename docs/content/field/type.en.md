---
title: 'Type'
date: 2019-02-14T14:02:24-05:00
weight: 5
---

A field's type defaults to `str`.

```python
from fire_odm import MemoryModel, Field

class Data(MemoryModel):
  name = Field()
```

A common practice is to use a built-in as a field type.

```python
from fire_odm import MemoryModel, Field

class Data(MemoryModel):
  name = Field(type=str)
```

A field type can be a function.

```python
from fire_odm import MemoryModel, field

def convert(value):
  if isinstance(value, int):
    return str(value)
  return value

class Data(MemoryModel):
  number = Field(type=convert)
```

A field type can be a method.

```python
from fire_odm import MemoryModel, Field

class Convert(object):

  @classmethod
  def method(cls, value):
    if isinstance(value, int):
      return str(value)
    return value

class Data(MemoryModel):
  number = Field(type=Convert.method)
```

A field type can be a string referring to a class's method.

```python
from fire_odm import MemoryModel, Field

class Data(MemoryModel):
  number = Field(type='convert')

  def convert(value):
    if isinstance(value, int):
      return str(value)
    return value
```

A field type can be a `Model`.

```python
from fire_odm import MemoryModel, Model, Field

class Name(Model):
  first = Field(required=True)
  last = Field(required=True)

class Data(MemoryModel):
  name = Field(type=Name)
```
