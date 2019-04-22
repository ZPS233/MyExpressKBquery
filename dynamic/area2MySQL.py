# -*- coding: utf-8 -*-
import json
import pymysql
with open('area-new-shentong.txt','r', encoding='UTF-8') as f:    
    areas = json.loads(f.read())

conn = pymysql.connect(host='localhost', user='root', passwd='123456', db='logistics', charset='utf8mb4', use_unicode=True)   
cursor = conn.cursor()
#provincesql = "INSERT INTO province(name, code) VALUES (%s,%s)"
#citysql = "INSERT INTO city(name, code, province_code) VALUES (%s,%s,%s)"
#countysql = "INSERT INTO county(name, code, city_code) VALUES (%s,%s,%s)"
#
#for p in areas:
#    cursor.execute(provincesql,(p['value'],int(p['code'])))
#    cities = p['childs']
#    for c in cities:
#        cursor.execute(citysql,(c['value'],c['code'],p['code']))
#        if 'childs' in c.keys():
#            counties = c['childs']
#            for county in counties:
#                cursor.execute(countysql,(county['value'],county['code'],c['code']))