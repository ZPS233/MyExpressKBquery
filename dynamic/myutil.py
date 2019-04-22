# -*- coding: utf-8 -*-
class area():
    
    @staticmethod
    #返回string
    def findCodeByName(provinceName,cityName,countyName,provinces):
        for p in provinces:
            if p['value'] == provinceName:
                provinceId = p['code']
                for city in p['childs']:
                    if city['value'] == cityName:
                        cityId = city['code']
                        if countyName != None:
                            for county in city['childs']:
                              if county['value'] == countyName:
                                  countyId = county['code']
                                  break
                        else:
                            countyId = None
                        break
                break
        return provinceId,cityId,countyId