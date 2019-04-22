# -*- coding: utf-8 -*-
import urllib
import json
general_place_url = 'http://www.sf-express.com/sf-service-owf-web/service/region/{}/subRegions?level={}&lang=sc&region=cn&translate='

overseas_url = 'http://www.sf-express.com/sf-service-owf-web/service/region/A000000000/subRegions/origins?level=-1&lang=sc&region=cn&translate='

#mainland = json.loads(urllib.request.urlopen(general_place_url.format('A000086000','-1')).read())
#gat = json.loads(urllib.request.urlopen(general_place_url.format('A000000000','-1')).read())

#包括中国 港澳台 和几个外国
overseas = json.loads(urllib.request.urlopen(overseas_url).read())

with open('./shunfeng_place.txt', 'w',encoding = 'utf-8') as f:
    for m in overseas:
#        print(m['name'],m['code'])
        f.write(m['name'] + ' '+ m['code'] + '\n')
        if m['name'] == '中国' or  m['name'] =='香港' or m['name'] == '台湾':
            if m['name'] == '中国':
                code = -1
            else:
                code = 2
            #省/直辖市
            subRegions = json.loads(urllib.request.urlopen(general_place_url.format(m['code'],code)).read())
            for subregion in subRegions:
#                print(subregion)
                if subregion['remark'] == None:
                    f.write('  '+subregion['name'] + ' '+ subregion['code'] +'\n')
                else:
                    f.write('  '+subregion['name'] + ' '+ subregion['code'] + ' ' + subregion['remark'] + '\n')
                #市
                subcitys = json.loads(urllib.request.urlopen(general_place_url.format(subregion['code'],'2')).read())
                for subcity in subcitys:
                    if subcity['remark'] == None:
                        f.write('    '+subcity['name'] + ' '+ subcity['code'] +'\n')
                    else:
                        f.write('    '+subcity['name'] + ' '+ subcity['code'] + ' ' + subcity['remark'] + '\n')
#                    print(subcity)
                    if subregion['name'][-1] != '市':
                        subblocks = json.loads(urllib.request.urlopen(general_place_url.format(subcity['code'],'3')).read())
                        for subblock in subblocks:
#                            print(subblock)
                            if subblock['remark'] == None:
                                f.write('      '+subblock['name'] + ' '+ subblock['code'] +'\n')
                            else:
                                f.write('      '+subblock['name'] + ' '+ subblock['code'] + ' ' + subblock['remark'] + '\n')
        elif m['name'] =='澳门':
            subRegions = json.loads(urllib.request.urlopen(general_place_url.format(m['code'],'2')).read())
            for subregion in subRegions:
#                print(subregion)
                if subregion['remark'] == None:
                    f.write('  '+subregion['name'] + ' '+ subregion['code'] +'\n')
                else:
                    f.write('  '+subregion['name'] + ' '+ subregion['code'] + ' ' + subregion['remark'] + '\n')