# -*- coding: utf-8 -*-
import urllib.request as request
import urllib.parse as parse
import json
import myutil
import time
    
with open('area-new-shentong.txt','r',encoding='UTF-8') as f:
    areas = json.loads(f.read())
    
class shentongDynamicQuery:
        
    @staticmethod
    def query_price(originprovinceName,origincityName,origincountyName,destprovinceName,destcityName,destcountyName,weight=0,time=None):
        url = 'http://www.sto.cn/Service/GetPriceMessage'
        originaddress = originprovinceName+'/'+origincityName+'/'+origincountyName
        destaddress = destprovinceName+'/'+destcityName+'/'+destcountyName
        data = {"StartCity":originaddress,"EndCity":destaddress,"Weight":weight,"StartDatetime":time}
        data = parse.urlencode(data).encode('utf-8')      
        req = request.Request(url, data=data)        
        result = json.loads(str(request.urlopen(req).read(),'utf-8'))
        service = result['Data']['data']
        s = dict()
        s['name'] = '申通快递'
        s['arriveDate'] = service['ageing']
        s['fee'] = service['price']
        return [s]
    
    
    @staticmethod
    def query_store(provinceName,cityName,countyName):
        storelist = []
        url = 'http://www.sto.cn/Site/GetOranizeByAreas'
        specificStoreURL = 'http://www.sto.cn/Site/GetOrganizeByCode?Code={}'
        pCode,cCode,dCode = myutil.area.findCodeByName(provinceName,cityName,countyName,areas)
        data = {'provinceId': pCode,"cityId": cCode,"districtId": dCode,"from":0,"size": 20}
        data = parse.urlencode(data).encode('utf-8')   
        req = request.Request(url, data=data)  
        result = json.loads(str(request.urlopen(req).read(),'utf-8'))
#        print(result)
        stores = result['Data']
        for store in stores:
            sCode = store['Code']
            htm_info = json.loads(str(request.urlopen(specificStoreURL.format(sCode)).read(),'utf-8'))
            s = htm_info['Data']
            d = dict()
            d['code'] = sCode
            d['name'] = s['FullName']
            d['countyCode'] = dCode
            d['cityCode'] = cCode
            d['provinceCode'] = pCode
            d['address'] = s['Address']
            d['distributionScope'] = s['DispatchRange']
            d['noDistributionScope'] = s['NotDispatchRange']
            d['manager'] = s['Manager']
            d['tel'] = s['ManagerMobile']
            d['businessScope'] = None
            storelist.append(d)
        print(len(storelist))
        return storelist

#print(shentongDynamicQuery.query_store('北京','北京市','大兴区'))     
present_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
print(shentongDynamicQuery.query_price('北京','北京市','大兴区','北京','北京市','大兴区',12,present_time))