---
title: 'Postgres'
date: 2020-02-01T20:20:48-05:00
weight: 15
---

## Example

Find all records in a table.

```python
from sugar_odm import PostgresDBModel, Field

class Model(PostgresDBModel):
  field = Field()

await Model.add([
  { 'field': 'alpha' },
  { 'field': 'beta' }
])

[ model async for model in Model.find() ]
```

## Query

Find a record using the `WHERE` clause.

```python
from sugar_odm import PostgresDBModel, Field

class Model(PostgresDBModel):
  field = Field()

await Model.add([
  { 'field': 'alpha' },
  { 'field': 'beta' }
])

[ model async for model in Model.find({ 'WHERE': 'data->>\'field\' = \'beta\'' }) ]
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
