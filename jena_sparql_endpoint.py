# -*- coding: utf-8 -*-
from SPARQLWrapper import SPARQLWrapper, JSON
from collections import OrderedDict

class JenaFuseki:
    def __init__(self, endpoint_url='http://localhost:3030/logistics/query'):
        self.sparql_conn = SPARQLWrapper(endpoint_url)

    def get_sparql_result(self, query):
        self.sparql_conn.setQuery(query)
        self.sparql_conn.setReturnFormat(JSON)
        return self.sparql_conn.query().convert()

    @staticmethod
    #解析返回结果
    def parse_result(query_result):
        try:
            query_head = query_result['head']['vars']
            query_results = list()
            for r in query_result['results']['bindings']:
                temp_dict = OrderedDict()
                for h in query_head:
                    temp_dict[h] = r[h]['value']
                query_results.append(temp_dict)
            return query_head, query_results
        except KeyError:
            return None, query_result['boolean']

    def print_result_to_string(self, query_result):
        """
        直接打印结果，用于测试
        :param query_result:
        :return:
        """
        query_head, query_result = self.parse_result(query_result)
        #判断是ASK还是SELECT
        if query_head is None:
            if query_result is True:
                print( 'Yes')
            else:
                print( 'False')
        else:
            for h in query_head:
                print(h, ' '*5)
            for qr in query_result:
                for _, value in qr.items():
                    print(value, ' ')

    def get_sparql_result_value(self, query_result):
        """
        用列表存储结果的值
        :param query_result:
        :return:
        """
        query_head, query_result = self.parse_result(query_result)
        if query_head is None:
            return query_result
        else:
            values = list()
            for qr in query_result:
                for _, value in qr.iteritems():
                    values.append(value)
            return values

# TODO 用于测试
if __name__ == '__main__':
    fuseki = JenaFuseki()
    my_query = """
PREFIX : <http://logistics#> 
PREFIX vocab: <http://logistics/vocab#> 
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#> 

ASK {
vocab:hasService   rdf:type rdf:Property.
}
limit 1000
    """
    result = fuseki.get_sparql_result(my_query)
    fuseki.print_result_to_string(result)