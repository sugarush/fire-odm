---
title: 'Postgres'
date: 2020-02-01T20:20:48-05:00
weight: 15
---

## Example

```python
from fire_odm import PostgresDBModel, Field

class Model(PostgresDBModel):
  field = Field()

await Model.add([
  { 'field': 'alpha' },
  { 'field': 'beta' }
])

[ model async for model in Model.find() ]
```

## Query

```python
from fire_odm import PostgresDBModel, Field

class Model(PostgresDBModel):
  field = Field()

await Model.add([
  { 'field': 'alpha' },
  { 'field': 'beta' }
])

[ model async for model in Model.find({ 'WHERE': 'data->>\'field\' = \'beta\'' }) ]
```

## Limit

```python
from fire_odm import PostgresDBModel, Field

class Model(PostgresDBModel):
  field = Field()

await Model.add([
  { 'field': 'alpha' },
  { 'field': 'beta' }
])

[ model async for model in Model.find(limit=1) ]
```

## Offset

```python
from fire_odm import PostgresDBModel, Field

class Model(PostgresDBModel):
  field = Field()

await Model.add([
  { 'field': 'alpha' },
  { 'field': 'beta' }
])

[ model async for model in Model.find(limit=1, skip=1) ]
```
