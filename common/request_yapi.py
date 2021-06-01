# !/usr/bin/python3
# -*-coding:utf-8-*-
# Author: Dragon
# CreatDate: 2020/12/30 15:15
import requests
import json

class Request_Yapi():


    def request_url_login():
        global header
        header = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
        yapi_login = 'http://10.39.39.13:443/api/user/login'
        postData = {
            "email": "admin@admin.com",
            "password": "ymfe.org",
        }
        responseRes = requests.post(yapi_login, data=postData, headers=header)
        return responseRes


    def request_url_data(json_data):
        Request_Yapi.request_url_login()
        for x in json_data:
            yapi_data = requests.get(x.api_url_json)
        yapi_json_data = json.loads(yapi_data.text)
        yapi_json_datas = yapi_json_data['message']
        fail_datas = []
        for x in yapi_json_data['list']:
            if x['status']!= 200:
                fail_datas.append(x)

        return yapi_json_datas,fail_datas

        

        



