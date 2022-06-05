class FilterModule(object):

    def filters(self):
        return {
            'axlquery2csv': self.axlquery2csv
        }

    def axlquery2csv(self, rows):
        if len(rows) < 1:
            return
        csv = ','.join( [ f'"{column_name}"' for column_name in list(rows[0].keys())] ) + '\n'
        for row in rows:
            csv += ','.join( [ f'"{column_name}"' for column_name in list(row.values())] ) + '\n'
        return csv