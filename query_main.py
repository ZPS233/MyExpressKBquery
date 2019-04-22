# encoding=utf-8
###第一步 把自然语言划分成一个个word对象  列表
###第二部 运用rule 的 apply 看哪条rule 正则表达 符合
###第三步 把符合的rule按符合的关键词多少排序 选最大的
###第四部 按照rule产生sparql查询语句


import jena_sparql_endpoint
import question2sparql

if __name__ == '__main__':
    #连接Fuseki服务器。
    fuseki = jena_sparql_endpoint.JenaFuseki()
    #初始化自然语言到SPARQL查询的模块，参数是外部词典列表。
    q2s = question2sparql.Question2Sparql(['./external_dict/company.txt','./external_dict/servicetype.txt','./external_dict/service.txt'])
    i =1
#    while True:
    while i <2 :
        i = i + 1
        question = input()
        my_query = q2s.get_sparql(question)
        print('查询语句:',my_query,'\n')
        if my_query is not None:
            result = fuseki.get_sparql_result(my_query)
#            value = fuseki.get_sparql_result_value(result)
            query_head, query_result = fuseki.parse_result(result)
            print('结果',query_head,query_result)
            if query_head is None:
                value =  query_result
            else:
                #查询单个属性 单个值
                if len(query_head) == 1 and len(query_result) == 1:
                    head = query_head[0]
                    print('question1-',query_result[0][head])
                #查询多个属性
                else:
                    print('question2-')
                    print(query_result)
#            # TODO 判断结果是否是布尔值，是布尔值则提问类型是"ASK"，回答“是”或者“不知道”。
#            if isinstance(value, bool):
#                if value is True:
#                    print ('Yes')
#                else:
#                    print ('I don\'t know. :(')
#            else:
#                # TODO 查询结果为空，根据OWA，回答“不知道”
#                if len(value) == 0:
#                    print ('I don\'t know. :(')
#                elif len(value) == 1:
#                    print (value[0])
#                else:
#                    output = ''
#                    for v in value:
#                        output += v + u'、'
#                    print (output[0:-1])

        else:
            # TODO 自然语言问题无法匹配到已有的正则模板上，回答“无法理解”
            print ('I can\'t understand.')
        print ('#' * 100)