class FilterModule(object):

    def filters(self):
        return {
            'axlquery2list': self.axlquery2list
        }

    def axlquery2list(self, xml):
        import xmltodict, json

        query_return=(xmltodict.parse(xml))['soapenv:Envelope']['soapenv:Body']['ns:executeSQLQueryResponse']['return']
        return json.dumps(query_return['row']) if query_return is not None else []