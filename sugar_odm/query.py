def pop_modifiers(d):
    results = { }
    for key in d:
        if key.startswith('$'):
            results[modifier] = d.pop(modifier)
    return results


class Query(dict):
    '''
    The Query class.

    :param table: The name of the table to query against.
    :param query: The JSON query statement.
    :param limit: The number of records to limit to.
    :param skip: The number of records to skip.
    '''

    def __init__(self, table=None, query={ }, limit=100, skip=0):
        if not table:
            raise Exception('Both table must be specified.')
        super(Query, self).__init__(query)
        self.table = table
        self.limit = limit
        self.skip = skip

    def to_postgres(self):
        '''
        Converts the `query` object to a **PostgreSQL** statement.
        '''
        query = f'SELECT data FROM {self.table} '
        arguments = [ ]
        count = 1

        if self:

            modifiers = pop_modifiers(self)

            if len(self) == 1:
                for (key, value) in self.items():
                    query += f'WHERE data->>${count} = ${count + 1} '
                    arguments.extend([ key, value ])
                    count += 2
            else:
                query += 'WHERE ('
                for (key, value) in self.items():
                    query += f'data->>${count} = ${count + 1} AND '
                    arguments.extend([ key, value ])
                    count += 2
                query = query[:-5] # remove the trailing ' AND '
                query += ') '

        query += f'LIMIT ${count}::bigint OFFSET ${count + 1}::bigint;'
        arguments.extend([ self.limit, self.skip ])

        return query, arguments
