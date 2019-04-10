# -*- coding: utf-8 -*-

from refo import finditer, Predicate, Star, Any, Disjunction
import re 

class W(Predicate):
    def __init__(self, token=".*", pos=".*"):
        self.token = re.compile(token + "$")
        self.pos = re.compile(pos + "$")
        super(W, self).__init__(self.match)
        print(self.pos,self.token)

    def match(self, word):
        m1 = self.token.match(word.token)
        m2 = self.pos.match(word.pos)
        return m1 and m2
pos_number = "m"
number_entity = (W(pos=pos_number))

adventure = W("冒险")