# -*- coding: utf-8 -*-

from flask import Flask, render_template,request
import jena_sparql_endpoint
import question2sparql

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
    q2s = question2sparql.Question2Sparql(['./external_dict/company.txt'])
    question = request.args.get('q')
    my_query = q2s.get_sparql(question)
    
    if my_query is not None:
        result = fuseki.get_sparql_result(my_query)
        value = fuseki.get_sparql_result_value(result)
        # TODO 判断结果是否是布尔值，是布尔值则提问类型是"ASK"，回答“是”或者“不知道”。
        if isinstance(value, bool):
            if value is True:
                return ('Yes')
            else:
                return ('I don\'t know. :(')
        else:
            # TODO 查询结果为空，根据OWA，回答“不知道”
            if len(value) == 0:
                return ('I don\'t know. :(')
            elif len(value) == 1:
                return (value[0])
            else:
                output = ''
                for v in value:
                    output += v + u'、'
                return (output[0:-1])
    else:
        # TODO 自然语言问题无法匹配到已有的正则模板上，回答“无法理解”
        return ('I can\'t understand.')
    
    
    
    
    return my_query


if __name__ == '__main__':
    app.run(port=5000, debug=True)