# encoding=utf-8
#将CSV文件转换为jieba外部词典的格式
import pandas as pd
import re

#company简称
#df = pd.read_csv('./company.csv')
#name = df['name'].values
#
#with open('./companyshortname.txt', 'a',encoding = 'utf-8') as f:
#    for t in name:
#        tt = re.search('(.*)(快递|快运|物流|速递|速运)',t)
#        if tt!= None:
#            t = tt.group(1)
#        f.write(t + '\n')

#servicetype
#df = pd.read_csv('./servicetype.csv')
#name = df['name'].values
#
#ns = []
#for t in name:
#    t = t.split('-')[1]
#    if t not in ns:
#        if ns == []:
#            ns.append(t)
#        else:
#            flag = 0 
#            for i in range(len(ns)):
#                if t[0:2] in ns[i]:
#                    ns.insert(i+1,t)
#                    flag = 1
#                    break
#            if flag == 0:
#                ns.append(t)
#            
#with open('./servicetype.txt', 'a',encoding = 'utf-8') as f:
#    for n in ns:
#        f.write(n + ' '+ 'nz' + '\n')


df = pd.read_csv('./service.csv')
name = df['name'].values

ns = []
for t in name:
    t = t.split('-')[1]
    if t not in ns:
        if ns == []:
            ns.append(t)
        else:
            flag = 0 
            for i in range(len(ns)):
                if t[0:2] in ns[i]:
                    ns.insert(i+1,t)
                    flag = 1
                    break
            if flag == 0:
                ns.append(t)
            
with open('./service.txt', 'a',encoding = 'utf-8') as f:
    for n in ns:
        f.write(n + ' '+ 'nz' + '\n')
