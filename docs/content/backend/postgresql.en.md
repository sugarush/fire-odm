---
title: 'PostgreSQL'
date: 2020-02-01T20:20:48-05:00
weight: 20
---

## Example

Find all records in a table.

```python
from sugar_odm import PostgresDBModel, Field

class Model(PostgresDBModel):

  __connection__ = {
    'user': 'username',
    'password': 'password',
    'host': 'localhost'
  }

  __database__ = {
    'name': 'postgres'
  }

  field = Field()

await Model.add([
  { 'field': 'alpha' },
  { 'field': 'beta' }
])

[ model async for model in Model.find() ]
```

## Query

Find a record using the _Model Query Language_ which is similar to the _MongoDB Query Language_:

```python
from sugar_odm import PostgresDBModel, Field

class Model(PostgresDBModel):
  field = Field()

await Model.add([
  { 'field': 'alpha' },
  { 'field': 'beta' }
])

[ model async for model in Model.find({ 'field': 'beta' }) ]
```

## Limit

Limit the number of results.

```python
from sugar_odm import PostgresDBModel, Field

class Model(PostgresDBModel):
  field = Field()

await Model.add([
  { 'field': 'alpha' },
  { 'field': 'beta' }
])

[ model async for model in Model.find(limit=1) ]
```

## Offset

Skip a number of results.

```python
from sugar_odm import PostgresDBModel, Field

class Model(PostgresDBModel):
  field = Field()

await Model.add([
  { 'field': 'alpha' },
  { 'field': 'beta' }
])

[ model async for model in Model.find(limit=1, skip=1) ]
```
