# -*- coding: utf-8 -*-
import re
import urllib.request as request
import urllib.parse as parse
import json

########{"value":,"code":,"children":[]}
#将韵达 old_place中的省加载并获取市 转换成json 存储到yunda_new_place中
#url = 'http://www.yundaex.com/ydweb/fuwuwangdian_area.php?act=get_shi&sheng_bm={}'
#countysURL = 'http://www.yundaex.com/cn/data/area.php'
#place = []
#with open('yunda_old_place.txt','r',encoding='UTF-8') as f:
#    lines = f.readlines()
#    for line in lines:
#        code = line[:6]
#        value = line[6:-1]
#        print(value)
##        print('##'*10,value)
#        childs = []
#        childResults = json.loads(request.urlopen(url.format(code)).read())
#        for result in childResults:
##            print('%%%%%%%',result['mc'])
#            subChilds = []
#            data = {'act': 'getCountys','id':result['bm']}
#            data = parse.urlencode(data).encode('utf-8')        
#            req = request.Request(countysURL, data=data)        
#            subChildResults = json.loads(str(request.urlopen(req,timeout = 50).read(),'utf-8'))
##            print(subChildResults)
#            for subChildResult in subChildResults:
#                subChilds.append({'code':subChildResult['id'],'value':subChildResult['name']})
#            childs.append({'code':result['bm'],'value':result['mc'],'child':subChilds})
#        place.append({'code':code,'value':value,'child':childs})
#
#print(place)
##json.dumps(place)
#with open('yunda_new_place.txt','w',encoding='UTF-8') as f:
#    f.write(json.dumps(place))

with open('yunda_new_place.txt','r',encoding='UTF-8') as f:
    provinces = json.loads(f.read())
    
class yundaDynamicQuery:
    
    @staticmethod
    #返回string
    def findIdbyName(provinceName,cityName,countyName=None):
        for p in provinces:
            if p['value'] == provinceName:
                provinceId = p['code']
                for city in p['child']:
                    if city['value'] == cityName:
                        cityId = city['code']
                        if countyName != None:
                            for county in city['child']:
                              if county['value'] == countyName:
                                  countyId = county['code']
                                  break
                        else:
                            countyId = None
                        break
                break
        return provinceId,cityId,countyId
    
    @staticmethod
    def query_price(originprovinceName,origincityName,origincountyName,destprovinceName,destcityName,destcountyName,weight=None,volume=0,time=None):
        url = 'http://www.yundaex.com/cn/data/search.php'
        oprovinceId,ocityId,odistrictId = yundaDynamicQuery.findIdbyName(originprovinceName,origincityName,origincountyName)
        dprovinceId,dcityId,ddistrictId = yundaDynamicQuery.findIdbyName(destprovinceName,destcityName,destcountyName) 
        if weight == None:
            weight = volume/6000
        data = {'act': 'Getyunfei','sp': oprovinceId,'ss': ocityId,'sx': odistrictId,'mp': dprovinceId,'ms':dcityId,'mx': ddistrictId,'zl': str(weight)}
        data = parse.urlencode(data).encode('utf-8')        
        req = request.Request(url, data=data)        
        result = str(request.urlopen(req).read(),'utf-8')
        return result
    
    
    @staticmethod
    #网点 code name cityCode provinceCode address distributionScope noDistributionScope manager tel
    #     bm   mc   shi      sheng        dz      psfw              bpsfw               fzr     cxdh
    def query_store(provinceName,cityName,keyword=''):
        #with open('yunda_store.txt','a',encoding = 'utf-8') as f:
            #f.write(provinceName+'-'+cityName+'\n')
            storeList = []
            url = 'http://www.yundaex.com/ydweb/fuwuwangdian_search.php?sheng={}&city={}&keywords={}&page={}'
            urlSpecificStoreInfo = 'http://www.yundaex.com/ydweb/fuwuwangdian_data.php?id={}'
            provinceId,cityId = yundaDynamicQuery.findIdbyName(provinceName,cityName)
            page = 1
            response = request.urlopen(url.format(provinceId,cityId,keyword,page)).read()
            result = re.search('yd_shi=(.*?)</script>',str(response,'utf-8')).group(1)
            jsondata = json.loads(result)
            stores = jsondata['datas']
            for store in stores:
                html_store_info = request.urlopen(urlSpecificStoreInfo.format(store['bm'])).read()
                data_store_info = re.search('yd_shi=(.*?)</script>',str(html_store_info,'utf-8')).group(1)
                data_store_info = re.sub('&(.*?);','',data_store_info)
                data_store_info = re.sub('【(.*?)】','',data_store_info)
                data_store_info = data_store_info.replace('br','').replace('strong','').replace('/','').replace('\\n','').replace('\u3000','').replace('nbsp;','')
                s = json.loads(data_store_info)
                d = dict()
                d['code'] = s['bm']
                d['name'] = s['mc']
                d['cityCode'] = s['shi']
                d['provinceCode'] = s['sheng']
                d['address'] = s['dz']
                d['distributionScope'] = s['psfw']
                d['noDistributionScope'] = s['bpsfw']
                d['manager'] = s['fzr']
                d['tel'] = s['cxdh']
                storeList.append(d)
                
            totals = int(jsondata['page']['totals'])
            perpagesize = int(jsondata['page']['perPageSize'])
            if totals == 0:
                pagenum = 1
            elif totals % perpagesize == 0:
                pagenum = int(totals/perpagesize)
            else:
                pagenum = int(totals/perpagesize) + 1
            print(pagenum)
            if pagenum > 1:
                for i in range(pagenum+1)[2:]:
                    print(i)
                    response = request.urlopen(url.format(provinceId,cityId,keyword,i),timeout = 1).read()
                    result = re.search('yd_shi=(.*?)</script>',str(response,'utf-8')).group(1)
                    jsondata = json.loads(result)
                    stores = jsondata['datas']
                    for store in stores:
                        html_store_info = request.urlopen(urlSpecificStoreInfo.format(store['bm'])).read()
                        data_store_info = re.search('yd_shi=(.*?)</script>',str(html_store_info,'utf-8')).group(1)
                        data_store_info = re.sub('&(.*?);','',data_store_info)
                        data_store_info = re.sub('【(.*?)】','',data_store_info)
                        data_store_info = data_store_info.replace('br','').replace('strong','').replace('/','').replace('\\n','').replace('\u3000','').replace('nbsp;','')
                        s = json.loads(data_store_info)
                        d = dict()
                        d['code'] = s['bm']
                        d['name'] = s['mc']
                        d['cityCode'] = s['shi']
                        d['provinceCode'] = s['sheng']
                        d['address'] = s['dz']
                        d['distributionScope'] = s['psfw']
                        d['noDistributionScope'] = s['npsfw']
                        d['manager'] = s['fzr']
                        d['tel'] = s['cxdh']
                        storeList.append(d)
            
            return storeList


#print(yundaDynamicQuery.query_store('山东省','东营市'))
#yundaDynamicQuery.query_store('北京市','(京)市辖区')
print(yundaDynamicQuery.query_price('山东省','东营市','利津县','山东省','东营市','河口区',2))