# sugar-odm

[![Build Status](https://travis-ci.com/sugarush/sugar-odm.svg?branch=master)](https://travis-ci.com/sugarush/sugar-odm)
[![codecov](https://codecov.io/gh/sugarush/sugar-odm/branch/master/graph/badge.svg)](https://codecov.io/gh/sugarush/sugar-odm)

## Documentation

[Documentation can be found here.](https://sugar-odm.docs.sugarush.io)

## Example

```python
from sugar_odm import PostgresDBModel, Field

class Model(PostgresDBModel):
  field = Field()

model = Model({ 'field': 'value' })

await model.save()

print(model.id)
```
