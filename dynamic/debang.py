# -*- coding: utf-8 -*-
import urllib.request as request
import json
import myutil
import time
import http.cookiejar

#with open('area-debang.txt','w',encoding='utf-8') as f:
#    htm = str(request.urlopen('https://www.deppon.com/newwebsite/assets/temp/pick-pcc.js').read(),'utf-8')
#    f.write(htm.replace('\n','').replace(' ','').split('*/')[1])
#修改area-debang.txt 只保留数据 
    
with open('area-debang.txt','r',encoding='UTF-8') as f:
    areas = json.loads(f.read())
    
headers = {
'Accept':'application/json, text/plain, */*',
'Origin':' https://www.deppon.com',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
'Content-Type':'application/json;charset=UTF-8',
'Referer':'https://www.deppon.com/newwebsite/mail/range',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'en,zh-CN;q=0.9,zh;q=0.8'
}
    
class debangDynamicQuery:
        
    @staticmethod
    ##"2019-04-20 11:04:47"  时间格式
    ##体积为立方米
    def query_price(originprovinceName,origincityName,origincountyName,destprovinceName,destcityName,destcountyName,weight=0,volume=0.001,time=None):
        url = 'https://www.deppon.com/phonerest/price/ordersFreightReckon'
        originaddress = originprovinceName+'-'+origincityName+'-'+origincountyName
        destaddress = destprovinceName+'-'+destcityName+'-'+destcountyName
        data = {"insuredAmount":0,"originalsaddress":originaddress,"originalsStreet":destaddress,"packageWeightFlag":0,"reviceMoneyAmount":0,"totalVolume":volume,"totalWeight":weight,"sendDateTime":time,"client":'true'}
        data = str(data).replace("'",'"').encode('utf-8')
        req = request.Request(url, data=data,headers = headers)        
        result = json.loads(str(request.urlopen(req).read(),'utf-8'))
        services = result['result']
        serviceList =[]
        for service in services:
            '''productName: "特准快件" arriveDate: "2019-04-21 07:30:00"days: "预计21号7:30前送达"
groundPrice: 11 ,lowerOfStage1: 1, lowerOfStage2: 30,detail: null, discount: null , heaveRate: null,label: "价格最优"
lightRate: null,message: null,omsProductCode: "DEAP",producteCode: "DEAP",rateOfStage1: 3,totalfee: 11,upperGround: 1'''
            s = dict()
            s['name'] = service['productName']
            s['arriveDate'] = service['arriveDate']
            s['fee'] = service['totalfee']
            serviceList.append(s)
        return serviceList
    
    
    @staticmethod
    def query_store(provinceName,cityName,countyName,keyword=''):
        storelist = []
        url = 'https://www.deppon.com/phonerest/branch/searchList'
        pCode,cCode,dCode = myutil.area.findCodeByName(provinceName,cityName,countyName,areas)
        data = {"cityCode": cCode,"countyCode": dCode,"keywords":keyword,"pageIndex":1,"pageSize": 200,"type": "1"}
        data = str(data).replace("'",'"').encode('utf-8')
        req = request.Request(url, data=data, headers = headers)  
        result = json.loads(str(request.urlopen(req).read(),'utf-8'))
        stores = result['result']['rows']
        for s in stores:
            #{'code''name''standardCode''deptAverage''address''phone' 'businessScope': '发货 提货 ''viewAverage'}
            d = dict()
            d['code'] = s['code']
            d['name'] = s['name']
            d['countyCode'] = dCode
            d['cityCode'] = cCode
            d['provinceCode'] = pCode
            d['address'] = s['address']
            d['distributionScope'] = None
            d['noDistributionScope'] = None
            d['manager'] = None
            d['tel'] = s['phone']
            d['businessScope'] = s['businessScope']
            storelist.append(d)
        return storelist

#print(debangDynamicQuery.query_store('北京','北京市','大兴区'))     
present_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
print(debangDynamicQuery.query_price('北京','北京市','大兴区','北京','北京市','大兴区',12,10,present_time))

##访问服务范围
#data = '{"cityCode":"110000-1","countyCode":"110115"}'.encode('utf-8') 
##cookie = http.cookiejar.CookieJar()  # 声明一个CookieJar对象实例来保存cookie
##handler = request.HTTPCookieProcessor(cookie)  # 利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
##opener = request.build_opener(handler)  # 通过handler来构建opener
#req = request.Request('https://www.deppon.com/phonerest/range/expressRange', data=data,headers = headers)  
##response = opener.open(req)
#print(str(request.urlopen(req).read(),'utf-8'))