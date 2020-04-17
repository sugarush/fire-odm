def pop_modifiers(d):
    results = { }
    for key in d:
        if key.startswith('$'):
            results[modifier] = d.pop(modifier)
    return results


class Query(dict):

    def __init__(self, table=None, query={ }, limit=100, skip=0):
        if not table:
            raise Exception('Both table and query must be specified.')
        super(Query, self).__init__(query)
        self.table = table
        self.limit = limit
        self.skip = skip

    def to_postgres(self):
        query = f'SELECT data FROM {self.table} '
        arguments = [ ]
        count = 1

        if self:

            modifiers = pop_modifiers(self)

            if len(self) == 1:
                for (key, value) in self.items():
                    query += f'WHERE data->>${count} = ${count + 1} '
                    arguments.extend([ key, value ])
            else:
                query += 'WHERE ('
                for (key, value) in self.items():
                    query += f'data->>${count} = ${count + 1} AND '
                    arguments.extend([ key, value ])
                    count += 2
                query = query[:-5] # remove the trailing ' AND '
                query += ') '

        query += f'LIMIT {self.limit} OFFSET {self.skip};'

        return query, arguments
