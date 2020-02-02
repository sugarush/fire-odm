---
title: 'Add Field'
date: 2020-02-01T19:36:51-05:00
weight: 1
---

The classmethod `add_field` exists to create recursive tree structures.

```python
from fire_odm import MemoryModel, Field

class Comment(MemoryModel):
  text = Field(required=True)

Comment.add_field('comments', Field(type=[ Comment ]))

comment = Comment({
  'text': 'hello',
  'comments': [
    {
      'text': 'world'
    }
  ]
})

comment # Prints <Comment:{ "comments": [ { "comments": [], "text": "world" } ], "text": "hello" }>
```
