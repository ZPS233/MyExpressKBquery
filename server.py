# -*- coding: utf-8 -*-

from flask import Flask, render_template,request
import jena_sparql_endpoint
import question2sparql
import json

#创建Flask实例对象,__name__作为程序名称,默认使用static目录存放静态资源，templates目录存放模板
app = Flask(__name__)



@app.route('/')
def home_page():
    return render_template('query.htm')
 
    

@app.route('/query',methods=['GET', 'POST'])
def query():
    #连接Fuseki服务器。
    fuseki = jena_sparql_endpoint.JenaFuseki()
    #初始化自然语言到SPARQL查询的模块，参数是外部词典列表。
    q2s = question2sparql.Question2Sparql(['./external_dict/company.txt','./external_dict/servicetype.txt','./external_dict/service.txt'])
    question = request.args.get('q')
    my_query = q2s.get_sparql(question)
    print('查询语句:',my_query,'\n')
    qtype = 1
    if my_query is not None:
        result = fuseki.get_sparql_result(my_query)
#        value = fuseki.get_sparql_result_value(result)
        #query_result为列表 元素是字典
        query_head, query_result = fuseki.parse_result(result)
        print('结果',query_head,query_result)
        if query_head is None:
            #ASK类型问题
            if query_result is True:
                answer = 'Yes' 
            else:
                answer = 'I don\'t know. :('
        else:
            if query_result == []:
                answer = 'I don\'t know. :('
                #查询单个属性 单个值
            else:
                if len(query_head) == 1 and len(query_result) == 1:
                    head = query_head[0]
                    answer = query_result[0][head]
                #查询多个属性
                else:
                    temp = list()
                    qtype = 2
                    for qr in query_result:
                        temp.append(json.dumps(qr))
                    return json.dumps({'type': qtype, 'head':query_head,'answer': temp})
    else:
        # TODO 自然语言问题无法匹配到已有的正则模板上，回答“无法理解”
        qtype = 0
        answer = 'I don\'t understand. :('
    return json.dumps({'type': qtype, 'answer': answer})


if __name__ == '__main__':
    app.run(port=5000, debug=True)