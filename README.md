# fire-odm

[![Build Status](https://travis-ci.com/sugarush/fire-odm.svg?branch=master)](https://travis-ci.com/sugarush/fire-odm)
[![codecov](https://codecov.io/gh/sugarush/fire-odm/branch/master/graph/badge.svg)](https://codecov.io/gh/sugarush/fire-odm)

## [Documentation](https://fire-odm.docs.sugarush.io)

## Example

```python
from fire_odm import PostgresDBModel, Field

class Model(PostgresDBModel):
  field = Field()

model = Model({ 'field': 'value' })

await model.save()

print(model.id)
```
