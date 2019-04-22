# -*- coding: utf-8 -*-
import urllib
import json
import time as Time
import datetime
import myutil

with open('area-zhongtong.txt','r', encoding='UTF-8') as f:    
    areas = json.loads(f.read())

class zhongtongDynamicQuery:
        
    @staticmethod
    def query_store(provinceName,cityName,districtName,keyword=''):
        storelist = []
        url = 'https://hdgateway.zto.com/Site_SearchGroupList'
        provinceId,cityId,districtId = myutil.area.findCodeByName(provinceName,cityName,districtName,areas)
        data = {'cityId':cityId, 'cityName': cityName , 'districtId': districtId,'districtName':districtName,'keyword':keyword,'provinceId':provinceId,'provinceName': provinceName}
        data = urllib.parse.urlencode(data).encode('utf-8')        
        req = urllib.request.Request(url, data=data)        
        result = json.loads(urllib.request.urlopen(req).read())
        if result['totalDisNum'] == None:
            return storelist
        else:
            for s in result['result']['items'][0]['list']:
                d = dict()
                d['companyName'] = '中通快递'
                d['code'] = s['code']
                d['name'] = s['fullName']
                d['countyName'] = districtName
                d['cityName'] = cityName
                d['provinceName'] = provinceName
                d['address'] = s['address']
                d['dispatchRange'] = s['dispatchRange']
                d['notDispatchRange'] = s['notDispatchRange']
                d['manager'] = s['manager']
                d['tel'] = 'masterMobile:'+str(s['masterMobile'])+' managerMobile:'+str(s['managerMobile'])+' outerPhone:'+str(s['outerPhone'])+' businessPhone:'+str(s['businessPhone'])
                d['businessScope'] = 'allowToPayment:'+s['allowToPayment']+' allowAgentMoney:'+s['allowAgentMoney']
                storelist.append(d)
        return storelist
        #{"result":null,"totalDisNum":null,"message":"查询结果为空！","statusCode":null,"status":false}
        '''{"result":{
                "items":[
                        {"districtName":"黄浦区","disNum":4,"list":[	
                                        多个{"allowAgentMoney":"1","code":"02104","distance":null,"latitude":31.233789,"companyName":"上海航空部","cityId":"310100","pic":null,"notDispatchRange":"0","pic1":null,"cityName":null,"id":3521,"fax":null,"pic2":null,"pic3":null,"pic4":null,"longitude":121.492367,
                                             "address":"上海市黄浦区人民路749号1楼中通快递","districtName":null,"manager":"姚卫国","managerMobile":"13817211798","fullName":"黄浦","provinceId":"310000","outerPhone":"021-63731851、17702182657","master":"姚卫国","dispatchRange":"新桥路，新昌路。","notDispatchRange"
                                             "districtId":"310101","masterMobile":"13370042585","allowToPayment":"1","provinceName":null,"businessPhone":"021-63731851、17317862038"},
                	                        ]
                	    }
                ]
            },
            "totalDisNum":4,
            "message":null,
            "statusCode":null,
            "status":true}'''
    
    @staticmethod
    #time 格式 "2019-04-20 11:04:47"
    def query_price(originprovinceName,origincityName,destprovinceName,destcityName,weight=0,volume=0,time=None):
        url ='https://hdgateway.zto.com/PriceAndHour_GetDomestic'
        oprovinceId,ocityId,odistrictId = myutil.area.findCodeByName(originprovinceName,origincityName,None,areas)
        dprovinceId,dcityId,ddistrictId = myutil.area.findCodeByName(destprovinceName,destcityName,None,areas)    
        weightV = volume/6000
        if weightV > weight:
            weight = weightV
        data = {'sendProvince':originprovinceName, 'sendProvinceCode': oprovinceId ,'sendCity':origincityName, 'sendCityCode': ocityId ,'destinationProvince':destprovinceName, 'destinationProvinceCode': dprovinceId ,'destinationCity':destcityName, 'destinationCityCode': dcityId,'weight':str(weight)}
        data = urllib.parse.urlencode(data).encode('utf-8')        
        req = urllib.request.Request(url, data=data)        
        result = json.loads(urllib.request.urlopen(req,timeout = 500).read())        
        
        y,m,d,H,M,S = Time.strptime(time, '%Y-%m-%d %H:%M:%S')[:6]
        time = datetime.datetime(y,m,d,H,M,S)
        arrivetime = time + datetime.timedelta(hours=+result['result']['hour'])
        
        s = dict()
        s['name'] = '中通快递'
        s['arriveDate'] = arrivetime.strftime('%Y-%m-%d %H:%M:%S')
        s['fee'] = result['result']['priceDisplay']
        return [s]
        
#present_time = Time.strftime("%Y-%m-%d %H:%M:%S", Time.localtime()) 
#print(zhongtongDynamicQuery.query_price('北京','北京市','天津','天津市',volume = 60000,time=present_time))    
#print(zhongtongDynamicQuery.query_store('宁夏回族自治区','银川市','兴庆区'))

import pymysql
with open('area-new-shentong.txt','r', encoding='UTF-8') as f:    
    areaDB = json.loads(f.read())
conn = pymysql.connect(host='localhost', user='root', passwd='123456', db='logistics', charset='utf8mb4', use_unicode=True)   
cursor = conn.cursor()
sql = '''INSERT INTO store(companyID, code, name, countyID, cityID, provinceID, address, dispatchRange, notDispatchRange, manager, tel, businessScope) 
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
for p in areas:
    for c in p['childs']:
        for county in c['childs']:
            if county['value'] == '其他区':
                break
            stores = zhongtongDynamicQuery.query_store(p['value'],c['value'],county['value'])
            if stores != []:
                try:                
                    provinceID,cityID,countyID = myutil.area.findCodeByName(stores[0]['provinceName'],stores[0]['cityName'],stores[0]['countyName'],areaDB)
                except:
                    with open('error.txt','a',encoding = 'utf-8') as f:
                        f.write(stores[0]['provinceName']+stores[0]['cityName']+stores[0]['countyName']+'\n')
            for d in stores:
                print(d)
                companyName = d['companyName']
                cursor.execute("SELECT company_id FROM company where company_chName = '"+companyName+"' ;")
                companyId = cursor.fetchone()
                cursor.execute(sql,(companyId,d['code'],d['name'],countyID, cityID, provinceID,d['address'],d['dispatchRange'],d['notDispatchRange'],d['manager'],d['tel'],d['businessScope'] ))
                
                    
cursor.close()
conn.commit()
conn.close()