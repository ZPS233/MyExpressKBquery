# encoding=utf-8
#将CSV文件转换为jieba外部词典的格式
import pandas as pd

df = pd.read_csv('./company.csv')
name = df['name'].values

with open('./company.txt', 'a',encoding = 'utf-8') as f:
    for t in name:
        f.write(t + ' ' + 'nt' + '\n')