# -*- coding: utf-8 -*-
import urllib
import json
import re
import time as Time
class shunfengDynamicQuery:
    
    @staticmethod
    #name 为xxshengxxshixxxian
    def query_store(name):
        storetype = {'1':'自营服务点','2':'外部合作点','5':'自助投递柜'}
        storeservice = {'1':'自寄服务','2':'自取服务','3':'寄、取件服务'}
        result = ''
        url = 'http://www.sf-express.com/sf-service-owf-web/service/store?lang=sc&region=cn&translate='\
        '&longitude={}&latitude={}&range=3000.0'        
        location_url = 'https://restapi.amap.com/v3/place/text?s=rsv3&children=&key=04e70f978f9d7314e3ef367f5071cf6c&offset=1&page=1&language=undefined&callback=jsonp_136338_&platform=JS&logversion=2.0&sdkversion=1.4.3&appname=http://www.sf-express.com/cn/sc/dynamic_function/store/&csid=4F4799C1-A0DF-4421-9E27-86636C67BDEF&keywords='
        location_response = urllib.request.urlopen(location_url+urllib.parse.quote(name)).read()
        temp = re.findall('location":"(.*?)",',str(location_response))[0]
        longtitude = temp.split(',')[0]
        latitude = temp.split(',')[1]
        stores = json.loads(urllib.request.urlopen(url.format(longtitude,latitude)).read())
        if stores == []:
            result = '暂无网点'
        else:
            for store in stores:
                result += ('网点代码:'+store['code'] + ' 名称:' + store['name']  + ' 地址:' +store['address'] + ' 联系人:' + store['linkman'] + ' 类型:'+ storetype[store['storeType']] +' 服务时间:' + store['serviceTime'] + ' 电话:' + store['tel'] + ' 服务:' )
                service = store['serviceContent'].split(',')
                print(service)
                for s in service:
                    if s!='':
                        result+= (storeservice[s]+',')
                result += '\n'
        return result
    
    
#       storeType 1 自营服务点 2 外部合作点 5自助投递柜 
#        外部合作点 所有带“SF”标识的便利店、洗衣店、高校、物业都是顺丰授权代办点，可免费为您提供寄件及代收件服务。
#        自营服务点 顺丰自营服务网点，提供自寄自取服务，大部分网点，自寄自取可享优惠。
#        自助投递柜 寄件无需下单、无需等收派员，随时寄件随时投递。
#       自寄自取享优惠  "selfSendDiscount":2.0,"selfPickupDiscount":2.0
#       顺丰大部分网点已开通自寄自取优惠服务，客户到指定网点自寄自取快件可享受立减运费或返电子优惠券。
#       serviceContent 1 自寄服务 2 自取服务 3 寄、取件服务        
#        [{"code":"SF76926995369","address":"东城区星城社区新世纪新城第一期9栋43号铺",
#         "deptCode":"769P","lat":22.815367,
#         "linkman":"范陈凌","lng":113.802724,"name":"(个体）新世纪星城便利店",
#         "serviceContent":"3","serviceTime":"08:00--20:00","serviceTime0":"",
#         "serviceTime6":"","serviceTime7":"","storeType":"2","tel":"0769-26995369",
#         "addressEN":""}]
    
    @staticmethod
    def query_china_range(code):
#        信息格式
#        {"type":"PART_REGION",
#         "unavailableRegions":[{"selfSend":false,"selfPickup":false,"name":"阿拉尔农场","code":"A659002016","availableAsOrigin":false,"availableAsDestination":false}],
#         "normalRegions":[{"selfSend":false,"selfPickup":false,"name":"金银川路街道","code":"A659002005","availableAsOrigin":true,"availableAsDestination":true}],
#         "abnormalRegions":[]}
        url = 'http://www.sf-express.com/sf-service-owf-web/service/region/{}/range?lang=sc&region=cn&translate='
        regions = json.loads(urllib.request.urlopen(url.format(code)).read())
        answer = ''
        if regions['type'] == 'ALL_REGION':
            answer += '全境提供服务\n'
        elif regions['type'] == 'PART_REGION':
            answer += '部分地区提供服务\n'
        if regions['unavailableRegions'] != []:
            answer += '不服务的地区为:'
            for region in regions['unavailableRegions']:
                answer = answer +  ' ' + region["name"]
        answer += '\n' 
        if regions['normalRegions'] != []:
            answer += '正常收送地区:'
            for region in regions['normalRegions']:
                answer = answer +  ' ' + region['name']
        return answer
    
    @staticmethod
    def query_global_range(code,zipcode):
        #信息格式 {"name":"澳大利亚","coverageRemark":null,"nonCoverageRemark":null}
        globalurl = 'http://www.sf-express.com/sf-service-owf-web/service/region/{}/globalRange?zipCode={}&lang=sc&region=cn&translate='
        try:
            response = urllib.request.urlopen(globalurl.format(code,zipcode))
            data = json.loads(response.read())
            if data['nonCoverageRemark'] == None:
                answer = '全境派送'
        except urllib.error.HTTPError:    # HTTP错误
            answer = '未找到该邮编配送信息，请致电客服中心'

        return answer
        
    @staticmethod
    def query_price(orginplacecode,destplacecode,weight,volume,time=0):
        prefixs = ['ratesByHeavyCargo?queryType=1','newRates?queryType=2','ratesByColdTransport?queryType=2&coolQueryType=1']
        url = 'http://www.sf-express.com/sf-service-owf-web/service/rate/{}'\
        '&origin={}&dest={}&weight={}&time={}&volume={}&lang=sc&region=cn&translate='
        #注意 时间 要以'2019-04-18T13:30:00+08:00'的形式 quote
        #weight =0 或 volume=0 [cm X cm X cm] 只要有一个有值就可以
        time = Time.strftime("%Y-%m-%dT%H:%M:%S+08:00", Time.localtime()) 
        timeurl = urllib.parse.quote(time)
        result = ''
#        print(url.format(prefixs[0],orginplacecode,destplacecode,weight,timeurl,volume))
        for prefix in prefixs:
            services = json.loads(urllib.request.urlopen(url.format(prefix,orginplacecode,destplacecode,weight,timeurl,volume)).read())
            for service in services:
                result += (service['limitTypeName']+service['deliverTime']+' '+str(service['freight'])+'\n')
            print(result)
        return result
        #数据格式
'''        [{"cargoTypeCode":"C201","cargoTypeName":"包裹","currencyName":"人民币","destCurrencyName":"人民币",
                 "destFreight":23.0,"destFuelCost":0.0,
                 "freight":23.0,"fuelCost":0.0,
                 "limitTypeCode":"T4","limitTypeName":"顺丰标快",
                 "weight":1.0,
                 "deliverTime":"2019-04-20 18:00","addTime":"2019-04-20 18:00",
                 "distanceTypeCode":"R10102","distanceTypeName":null,"expectArriveTm":null,"otherService":null,
                 "internet":false,"closedTime":"","orgionView":"1","destView":"1",
                 "destFuelFlg":true,"weightUnit":"kg","destWeightUnit":"kg",
                 "destWeight":1.0,"regionFreight":0.0,"totalFreight":23.0,
                 "productCode":"S1","expressTypeCode":"B1",
                 "pickupFreight":0.0,"destPickupFreight":0.0,"transportFreight":23.0,"destTransportFreight":23.0,"distributionFreight":0.0,"destDistributionFreight":0.0}]'''
        
#print(shunfengDynamicQuery.query_china_range('A110106000'))
#print(shunfengDynamicQuery.query_global_range('A000061000','1430'))
#print(shunfengDynamicQuery.query_global_range('A000061000','143'))
        
#print(shunfengDynamicQuery.query_store('河北省保定市安国市'))
print(shunfengDynamicQuery.query_price('A130683000','A440320000','10','0'))