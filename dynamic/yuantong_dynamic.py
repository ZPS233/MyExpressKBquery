# -*- coding: utf-8 -*-
import re
import urllib.request as request
import urllib.parse as parse
import json

#places = []
#provinces = {"北京":3110101,"上海":3310101,"天津":3120101,"重庆":3500101,"江苏":2320102,"浙江":2330102,"安徽":2340102,"河北":2130102,"河南":2410102,"湖北":2420102,"湖南":2430482,"江西":2360203,"广东":2440103,"黑龙江":2230102,"吉林":2220102,"辽宁":2210102,"山东":2370102,"山西":2140121,"陕西":2610102,"四川":2510104,"青海":2630102,"甘肃":2620421,"贵州":2520102,"福建":2350102,"云南":2530102,"海南":2460105,"新疆":2650102,"内蒙古":2150102,"西藏":2540102,"广西":2450102,"宁夏":2640104,"香港":"8a8142c3324990c7013266ba4f9e5030"}
#url = 'http://www.yto.net.cn/api/base/citys/bypid'
#for province in provinces.items():
#    print(province)
#    data = parse.urlencode({'id':province[1]}).encode('utf-8')        
#    req = request.Request(url, data=data)        
#    result = json.loads(str(request.urlopen(req).read(),'utf-8'))
#    childs = []
#    for child in result['data']:
#        childs.append({'code':child['id'],'value':child['name']})
#    places.append({'code':province[1],'value':province[0],'child':childs})
#
#with open('yuantong_place.txt','w',encoding='UTF-8') as f:
#    f.write(json.dumps(places))

with open('yuantong_place.txt','r',encoding='UTF-8') as f:
    provinces = json.loads(f.read())

with open('yunda_new_place.txt','r',encoding='UTF-8') as f:
    new_provinces = json.loads(f.read())
        

class yuantongDynamicQuery:
    
    @staticmethod
    def findIdbyName(provinceName,cityName):
        for p in provinces:
            if p['value'] == provinceName:
                provinceId = p['code']
                for city in p['child']:
                    if city['value'] == cityName:
                        cityId = city['code']
                        break
                break
        return provinceId,cityId
    
    
    @staticmethod
    #返回string
    def newFindIdbyName(provinceName,cityName):
        for p in new_provinces:
            if p['value'] == provinceName:
                provinceId = p['code']
                for city in p['child']:
                    if city['value'] == cityName:
                        cityId = city['code']
                        break
                break
        return provinceId,cityId
    
    @staticmethod
    def query_price(originprovinceName,origincityName,destprovinceName,destcityName,weight,length=0,width=0,height=0):
        url = 'http://www.yto.net.cn/api/base/freight'
        oprovinceId,ocityId = yuantongDynamicQuery.newFindIdbyName(originprovinceName,origincityName)
        dprovinceId,dcityId = yuantongDynamicQuery.newFindIdbyName(destprovinceName,destcityName) 
        data = {'fromLabel':None ,'fromProvinceCode': str(oprovinceId),'fromProvinceName':originprovinceName,
                'fromCityCode': ocityId,'fromCityName': origincityName,'toLabel': None, 'toProvinceCode':dprovinceId,
                'toProvinceName':destprovinceName, 'toCityCode':dcityId,'toCityName':destcityName,'weight': weight,'length':length,'width':weight,'height':height}
        print(data)
        data = parse.urlencode(data).encode('utf-8')        
        req = request.Request(url, data=data)        
        result = json.loads(str(request.urlopen(req).read(),'utf-8'))
        return result
    
    
    @staticmethod
    #网点 code name cityCode provinceCode address distributionScope noDistributionScope manager tel
    def query_store(provinceName,cityName):
        url = 'http://www.yto.net.cn/api/base/station/bycityid'
        specificStoreURL = 'http://www.yto.net.cn/api/base/station/detail/bycode'
        provinceId,cityId = yuantongDynamicQuery.findIdbyName(provinceName,cityName)
        data = {'cityId':cityId}
        data = parse.urlencode(data).encode('utf-8')        
        req = request.Request(url, data=data)        
        result = json.loads(str(request.urlopen(req).read(),'utf-8'))
        stores = result['data']
        print(stores)
        storeList = []
        for store in stores:
            data2 = {'cityId':cityId,'code':store['code']}
            data2 = parse.urlencode(data2).encode('utf-8')        
            req2 = request.Request(specificStoreURL, data=data2)        
            result2 = json.loads(str(request.urlopen(req2).read(),'utf-8'))
            storeInfo = result2['data']
            '''{'handlerName': '陈跃群', 
            'email': None, 'msn': None, 'fax': '021-62113021', 'queryTel': '长宁区东部查询电话：021-62139830   62101790;客服电话:021-62139830   62101790;取件电话：021-62139830  62101790  62113021;投诉电话:021-62101790', 
            'serveArea': '全境<br/>', 
            'stopArea': '无', 
            'serveDate': None, 
            'serveDay': None, 
            'especialServe': None, 
            'createTimeStation': '2018-12-10', 
            'remark': '-', 
            'stationOutName': '长宁区东部', 'pathName': '中国,上海,上海市,长宁区', 
            'stationName': '上海市长宁区东部', 'display': '1', 'parentId': '210901', 
            'serveTel': None, 'specialArea': None, 'selfArea': None, 'codesFenBu': None}'''
            d = dict()
            d['code'] = store['code']
            d['name'] = storeInfo['stationName']
            d['cityCode'] = cityId
            d['provinceCode'] = provinceId
            d['address'] = storeInfo['pathName']
            d['distributionScope'] = storeInfo['serveArea']
            d['noDistributionScope'] = storeInfo['stopArea']
            d['manager'] = storeInfo['handlerName']
            d['tel'] = storeInfo['queryTel']
            storeList.append(d)
        return storeList
        
        
#print(yuantongDynamicQuery.query_store('上海','长宁区'))
print(yuantongDynamicQuery.query_price('江苏省','南京市','山东省','东营市','10'))

#fromLabel: 
#fromProvinceCode: 110000
#fromProvinceName: 北京
#fromCityCode: 110101
#fromCityName: 东城区
#toLabel: 
#toProvinceCode: 370000
#toProvinceName: 山东省
#toCityCode: 370500
#toCityName: 东营市

        
        
        
        
        
        
        
        
        
        
        
        
        