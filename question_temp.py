# encoding=utf-8

from refo import finditer, Predicate, Star, Any
import re

#SPARQL前缀和模板
SPARQL_PREXIX = """
PREFIX : <http://logistics#> 
PREFIX vocab: <http://logistics/vocab#> 
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
"""

SPARQL_SELECT_TEM = "{prefix}\n" + \
             "SELECT DISTINCT {select} WHERE {{\n" + \
             "{expression}\n" + \
             "}}\n"

SPARQL_COUNT_TEM = "{prefix}\n" + \
             "SELECT COUNT({select}) WHERE {{\n" + \
             "{expression}\n" + \
             "}}\n"

SPARQL_ASK_TEM = "{prefix}\n" + \
             "ASK {{\n" + \
             "{expression}\n" + \
             "}}\n"

class W(Predicate):
    def __init__(self, token=".*", pos=".*"):
        self.token = re.compile(token + "$")
        self.pos = re.compile(pos + "$")
        super(W, self).__init__(self.match)

    def match(self, word):
        m1 = self.token.match(word.token)
        m2 = self.pos.match(word.pos)
        return m1 and m2


class Rule(object):
    def __init__(self, condition_num, condition=None, action=None):
        assert condition and action
        self.condition = condition
        self.action = action
        self.condition_num = condition_num

    def apply(self, sentence):
        matches = []
        #拿着分好的词(整个输入的句子)   去跟 规则进行匹配    只留下匹配到的词(中间可能包含其他杂项)   
        #如果一个句子中包含多个符合规则的短句,则将多个子句返回给action函数 但是只处理第一个子句
        for m in finditer(self.condition, sentence):
            i, j = m.span()
            matches.extend([sentence[i:j]])
        return self.action(matches), self.condition_num

class QuestionSet:
    def __init__(self):
        pass

    @staticmethod
    def has_company_basicinfo_question(clauses):
        print('\n与企业属性规则匹配')
        #公司属性
        select = "?x"
        sparql = None
        for i,clause in enumerate(clauses):
            print('问题子句',i,':')
            keyword = None
            matches = []
            for index,cbW in enumerate(listW_company_basic):
                for m in finditer(cbW, clause):
                    i, j = m.span()
                    matches.extend(clause[i:j])
                    if len(matches) != 0:
                        keyword = keyWord_company_baisc[index]
                if keyword is not None:
                    break

            for w in clause:
                if w.pos == pos_company:
                    if keyword == 'company_description':
#                        select = "?x ?y"
#                        e = "?s vocab:company_chName '{company_name}'."\
#                            "?s vocab:company_baidubaikeDescription ?x."\
#                            "?s vocab:company_kuaidi100Description ?y.".format(company_name=w.token)
                        select = "?y"
                        e = "?s vocab:company_chName '{company_name}'."\
                            "?s vocab:company_kuaidi100Description ?y.".format(company_name=w.token)
                    else:
                        e = "?s vocab:company_chName '{company_name}'."\
                            "?s vocab:{keyword} ?x.".format(company_name=w.token, keyword=keyword)
                    sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX, select=select, expression=e)
                    break
        return sparql
        
    @staticmethod
    def has_companyOrPerson_all_basicinfo_question(clauses):
        #人/公司 全部属性
        print('\n与企业的全部属性规则匹配')
        select = "?subject ?predicatelabel ?object"
        sparql = None
        for i,clause in enumerate(clauses):
            print('问题子句',i,':')
            for w in clause:
                if w.pos == pos_company :
                    e = "?s vocab:company_chName '{company_name}'."\
                        "?s ?predicate ?object."\
                        "?s rdfs:label ?subject."\
                        "?predicate rdfs:label ?predicatelabel".format(company_name=w.token)                
                elif w.pos == pos_person:
                    e = "?subject vocab:person_chName '{person_name}'."\
                        "?subject ?predicate ?object."\
                        "?predicate rdfs:label ?predicatelabel".format(person_name=w.token)
                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX, select=select, expression=e)
                break
            return sparql

    @staticmethod
    def has_servicetype_question(clauses):
        #企业 服务类型
        print('\n与企业服务类型规则匹配')
        select = "?servicetype"
        sparql = None
        for i,clause in enumerate(clauses):
            print('问题子句',i,':')
            for w in clause:
                if w.pos == pos_company:
                    e = "?s vocab:company_chName '{company_name}'."\
                            "?s vocab:hasServiceType ?st."\
                            "?st rdfs:label ?servicetype.".format(company_name=w.token)
                    sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX, select=select, expression=e)
                    break
        return sparql

    @staticmethod
    def has_specific_servicetype_question(clauses):
        #具体类型 的 服务service
        print('\n与企业具体服务类型规则匹配')
        select = "?ss"
        sparql = None
        matches = []
        keyword = None
        for i,clause in enumerate(clauses):
            print('问题子句',i,':')
            for index,stW in enumerate(listW_servicetype):
                for m in finditer(stW, clause):
                    i, j = m.span()
                    matches.extend(clause[i:j])
                    if len(matches) != 0:
                        keyword = keywords_servicetype[index]
                if keyword is not None:
                    break
            print(keyword)
            for w in clause:
                if w.pos == pos_company:
                    e = "?s vocab:company_chName '{company_name}'."\
                            "?s vocab:hasServiceType ?st."\
                            "?st vocab:servicetype_name '{servicetype_name}'."\
                            "?st vocab:hasService ?service."\
                            "?service vocab:service_name ?ss".format(company_name=w.token,servicetype_name=w.token+'-'+keyword)
                    sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX, select=select, expression=e)
                    break
        return sparql
    
    @staticmethod
    def has_service_question(clauses):
        #企业 服务
        print('\n与企业服务规则匹配')
        select = "?ss"
        sparql = None
        for i,clause in enumerate(clauses):
            print('问题子句',i,':')
            for w in clause:
                if w.pos == pos_company:
                    e = "?s vocab:company_chName '{company_name}'."\
                        "?s vocab:hasServiceType ?st."\
                        "?st vocab:hasService ?service."\
                        "?service vocab:service_name ?ss".format(company_name=w.token)
                    sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX, select=select, expression=e)
                    break
        return sparql

    @staticmethod
    def has_specific_service_question(clauses):
        #具体类型 的 服务service
        print('\n与企业具体服务规则匹配')
        select = "?siname ?sidesc"
        sparql = None
        matches = []
        keyword = None
        for i,clause in enumerate(clauses):
            print('问题子句',i,':')
            for index,sW in enumerate(listW_service):
                for m in finditer(sW, clause):
                    i, j = m.span()
                    matches.extend(clause[i:j])
                    if len(matches) != 0:
                        keyword = keywords_service[index]
                if keyword is not None:
                    break
            for w in clause:
                if w.pos == pos_company:
                    e = "?s vocab:company_chName '{company_name}'."\
                            "?s vocab:hasServiceType ?st."\
                            "?st vocab:hasService ?service."\
                            "?service vocab:service_name '{service_name}'."\
                            "?service vocab:hasServiceItem ?si."\
                            "?si vocab:serviceitem_name ?siname."\
                            "?si vocab:serviceitem_description ?sidesc".format(company_name=w.token,service_name=w.token+'-'+keyword)
                    sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX, select=select, expression=e)
                    break
        return sparql

    @staticmethod
    def has_compare_question(word_objects):
        """
        某演员参演的评分高于X的电影有哪些？
        :param word_objects:
        :return:
        """
        select = u"?x"

        person = None
        number = None
        keyword = None

#        for r in compare_keyword_rules:
#            keyword = r.apply(word_objects)
#            if keyword is not None:
#                break

        for w in word_objects:
            if w.pos == pos_person:
                person = w.token

            if w.pos == pos_number:
                number = w.token

        if person is not None and number is not None:

            e = u"?p :personName '{person}'." \
                u"?p :hasActedIn ?m." \
                u"?m :movieTitle ?x." \
                u"?m :movieRating ?r." \
                u"filter(?r {mark} {number})".format(person=person, number=number,
                                                     mark=keyword)

            return SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                            select=select,
                                            expression=e)
        else:
            return None


    @staticmethod
    def is_comedian_question(word_objects):
        """
        某演员是喜剧演员吗
        :param word_objects:
        :return:
        """
        sparql = None
        for w in word_objects:
            if w.pos == pos_person:
                e = u"?s :personName '{person}'." \
                    u"?s rdf:type :Comedian.".format(person=w.token)

                sparql = SPARQL_ASK_TEM.format(prefix=SPARQL_PREXIX, expression=e)
                break

        return sparql


#字符串列表 keyword用于sql
keywords_service = []
listW_service= []
with open('external_dict/service.txt','r',encoding = 'utf-8') as f:
    lines = f.readlines()
    for line in lines:
        print(line)
        keywords_service.append(line.split(' ')[0])

#用于问题匹配
words_service = W(keywords_service[0])
#用于匹配到后 找到是哪一个serviceType
listW_service.append(W(keywords_service[0]))
for st in keywords_service[1:]:
    words_service = words_service|W(st)
    listW_service.append(W(st))     


#字符串列表 keyword用于sql
keywords_servicetype = []
listW_servicetype= []
with open('external_dict/servicetype.txt','r',encoding = 'utf-8') as f:
    lines = f.readlines()
    for line in lines:
        print(line)
        keywords_servicetype.append(line.split(' ')[0])

#用于问题匹配
words_servicetype = W(keywords_servicetype[0])
#用于匹配到后 找到是哪一个serviceType
listW_servicetype.append(W(keywords_servicetype[0]))
for st in keywords_servicetype[1:]:
    words_servicetype = words_servicetype|W(st)
    listW_servicetype.append(W(st))         

# TODO 定义关键词
pos_company = 'nt'
pos_person = "nr"
pos_service = "nz"
pos_servicetype = 'nz'
pos_number = "m"

company_servicetype =  (W(pos = pos_servicetype))
company_service =  (W(pos = pos_service))
company_entity = (W(pos = pos_company))
person_entity = (W(pos=pos_person))
number_entity = (W(pos=pos_number))

english_name = (W("英文名") | W("英文") + W("名字"))

actor = (W("演员") | W("艺人") | W("表演者"))
movie = (W("电影") | W("影片") | W("片子") | W("片") | W("剧"))
category = (W("类型") | W("种类"))
several = (W("多少") | W("几部"))

higher = (W("大于") | W("高于"))
lower = (W("小于") | W("低于"))
compare = (higher | lower)

birth = (W("生日") | W("出生") + W("日期") | W("出生"))
birth_place = (W("出生") | W("出生")+W(""))

introduction = (W("介绍") | W("是") + W("谁") | W("简介"))
person_basic = (birth | birth_place | english_name | introduction)

rating = (W("评分") | W("分") | W("分数"))
release = (W("上映"))
movie_basic = (rating | introduction | release)

company_tel = W('电话')
company_web = (W('官网')|W('网页'))
company_description = (W("介绍") | W("简介"))
company_businessScope = W("经营范围")
word_service = W("服务")
word_type = W("类型")
company_slogan = W("口号")
company_annualTurnover = W("年")+W("营业额")
company_chairMan = W("董事长")
incorporate = (W("成立")|W("创办"))
headquarter =  (W("总部") | W("总部")+W('地址'))
incorporation_time= incorporate + (W("日期")|W("时间"))
company_basic = (incorporation_time|headquarter|english_name|company_description|company_businessScope|word_type|company_slogan|company_annualTurnover|company_chairMan)

when = (W("何时") | W("时候"))
where = (W("哪里") | W("哪儿") | W("何地") | W("何处") | W("在") + W("哪"))


listW_company_basic = [company_tel,company_web,incorporation_time,headquarter,english_name,company_description,company_businessScope,word_type,company_slogan,company_annualTurnover,company_chairMan]
keyWord_company_baisc = ['company_tel','company_website','company_incorporationTime','company_headquarter','company_enName','company_description','company_businessScope','company_type','company_slogan','company_annualTurnover','company_chairMan']

# TODO 问题模板/匹配规则
"""
1.某company的英文名 经营范围 公司类型 公司口号 年营业额 董事长 成立时间 总部地址 电话 网站
2.某company的成立时间[什么时候/何时成立?]
3.某person/company
4.某company提供/有  哪些类型的服务/服务的类型
5.某company 有哪些 XX 类型 的 服务 (有哪些)
6.某company提供/有  哪些服务
7.某company XX 服务


7. 某演员出演了多少部电影。
8. 某演员是喜剧演员吗。
"""
rules = [
    Rule(condition_num=2, condition=company_entity + Star(Any(), greedy=False) + company_basic + Star(Any(), greedy=False), action = QuestionSet.has_company_basicinfo_question ),
    Rule(condition_num=2, condition=company_entity + Star(Any(), greedy=False) + when + incorporate + Star(Any(), greedy=False),action=QuestionSet.has_company_basicinfo_question),
    
    Rule(condition_num=1, condition=Star(Any(), greedy=False) + (company_entity|person_entity) + Star(Any(), greedy=False), action = QuestionSet.has_companyOrPerson_all_basicinfo_question ),
    #4
    Rule(condition_num=3, condition=company_entity + Star(Any(), greedy=False) + (word_type+Star(Any(), greedy=False)+word_service|word_service+Star(Any(), greedy=False)+word_type), action = QuestionSet.has_servicetype_question),
    #5
    Rule(condition_num=4, condition=company_entity + Star(Any(), greedy=False) + words_servicetype + word_type + Star(Any(), greedy=False) + word_service, action = QuestionSet.has_specific_servicetype_question),
    #6
    Rule(condition_num=2, condition=company_entity + Star(Any(), greedy=False) + word_service, action = QuestionSet.has_service_question),
    #7
    Rule(condition_num=3, condition=company_entity + Star(Any(), greedy=False) + words_service + word_service, action = QuestionSet.has_specific_service_question),
    
    
    Rule(condition_num=4, condition=person_entity + Star(Any(), greedy=False) + compare + number_entity + Star(Any(), greedy=False) + movie + Star(Any(), greedy=False), action=QuestionSet.has_compare_question),
]