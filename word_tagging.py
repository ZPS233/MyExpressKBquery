# encoding=utf-8
#定义Word类;定义Tagger类;实现语句转为Word对象
import jieba
import jieba.posseg as pseg

class Word(object):
    def __init__(self, token, pos):
        self.token = token
        self.pos = pos
    def __str__(self):
        return '词:'+self.token+'  词性:'+self.pos

class Tagger:
    #加载外部词典
    def __init__(self, dict_paths):
        for p in dict_paths:
            jieba.load_userdict(p)
        jieba.suggest_freq(('服务','类型'), True)
#        jieba.suggest_freq(('时效','件'), True)
        #jieba.suggest_freq(('', ''), True)

    @staticmethod
    #把自然语句转化为word对象
    def get_word_objects(sentence):
        # type: (str) -> list
        return [Word(word, tag) for word, tag in pseg.cut(sentence)]

#测试
if __name__ == '__main__':
    tagger = Tagger(['external_dict/company.txt'])
    s = input()
    for i in tagger.get_word_objects(s):
        print (i.token, i.pos)