About
=====

Sugar ODM is an Object Document Mapper with backends for **Memory**,
**PostgreSQL**, **MongoDB** and **RethinkDB**.

Installation
------------

Sugar ODM can be installed with `pip`:

``pip install git+https://github.com/sugarush/sugar-odm@master``

Usage
-----

.. code-block:: python

  from sugar_odm import MemoryModel, Field

  class DataModel(MemoryModel):
    field = Field()

  model = DataModel({ 'field': 'value' })

  assert model.field == 'value'

  await model.save()

  assert model.id != None
