# encoding=utf-8
import question_temp
import word_tagging

class Question2Sparql:
    def __init__(self, dict_paths):
        self.wt = word_tagging.Tagger(dict_paths)
        self.rules = question_temp.rules
    #调用语句分词函数,找到匹配的模板，返回对应的SPARQL查询语句
    def get_sparql(self, question):
        word_objects = self.wt.get_word_objects(question)
        
        print('分词结果:')
        for word in word_objects:
            print(word)
        print('与rules的匹配结果:')
        
        queries_dict = dict()
        #将分好的word对象作为sentence传入
        for rule in self.rules:
            query, num = rule.apply(word_objects)
            print(query,num)
#            print(query,num)
            if query is not None:
                queries_dict[num] = query
        
        print('词典:',queries_dict)
                
                
        if len(queries_dict) == 0:
            return None
        elif len(queries_dict) == 1:
            return list(queries_dict.values())[0]
        else:
            #以匹配关键词最多的句子作为返回结果
            sorted_dict = sorted(queries_dict.items(), key=lambda item: item[0], reverse=True)
            return sorted_dict[0][1]