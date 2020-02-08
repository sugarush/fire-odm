---
title: 'MongoDB'
date: 2020-02-01T20:20:43-05:00
weight: 10
---

## Query

[Here](https://pymongo.readthedocs.io/en/3.10.0/api/pymongo/collection.html#pymongo.collection.Collection.find)
is the documentation for **PyMongo's** `find` method.

## Example

```python
from sugar_odm import MongoDBModel, Field

class Model(MongoDBModel):

  __index__ = [
    # Motor indices.
    {
      'keys': [('field', 'text')]
    }
  ]

  __connection__ = {
    # Motor connection options.
  }

  __database__ = {
    # Motor database options.
    'name': 'test'
  }

  __collection__ = {
    # Motor collection options.
    'name': 'my-collection-name'
  }

  field = Field()

await Model.add([
  { 'field': 'alpha beta' },
  { 'field': 'beta gamma' }
])

[ model async for model in Model.find({ '$text': { '$search': 'beta' } }) ]
```

## Filter

Specifies the documents to be returned.

```python
from sugar_odm import MongoDBModel, Field

class Model(MongoDBModel):
  field = Field()

await Model.add([
  { 'field': 'alpha' },
  { 'field': 'beta' }
])

[ model async for model in Model.find({ 'field': 'beta' }) ]
```

## Limit

Limits the number of results.

```python
from sugar_odm import MongoDBModel, Field

class Model(MongoDBModel):
  field = Field()

await Model.add([
  { 'field': 'alpha' },
  { 'field': 'beta' }
])

[ model async for model in Model.find(limit=1) ]
```

## Skip

Skips a number of records.

```python
from sugar_odm import MongoDBModel, Field

class Model(MongoDBModel):
  field = Field()

await Model.add([
  { 'field': 'alpha' },
  { 'field': 'beta' }
])

[ model async for model in Model.find(limit=1, skip=1) ]
```

## Projection

The fields which should be returned.

```python
from sugar_odm import MongoDBModel, Field

class Model(MongoDBModel):
  field = Field()

await Model.add([
  { 'field': 'alpha' },
  { 'field': 'beta' }
])

[ model async for model in Model.find(projection={ 'field': 1 }) ]
```
