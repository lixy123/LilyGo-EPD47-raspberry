#! /usr/bin/python
# coding = utf-8
#import urllib.request
import requests

import json
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit'
                      '/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safar'
                      'i/537.36',
    }
def GetWeatherInfo():
    #ApiUrl= \
    ApiUrl= "http://api.jisuapi.com/weather/query?appkey=***&cityid=1"            
    try:
        #print ApiUrl
        resp=requests.get(ApiUrl, headers=headers)
        resp.encoding = 'utf-8'
        #将JSON编码的字符串转换回Python数据结构
        jsonArr=json.loads(resp.text)
        #output result of json
        return jsonArr
    except:
        print ("error!")
        return None


