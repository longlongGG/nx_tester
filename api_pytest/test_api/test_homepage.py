#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Dragon
# @Software: PyCharm
#首页接口自动化
import requests

from api_pytest.test_api.yamls_unit.yaml_unit import read_yaml
import pytest

class TestHomePage:
    @pytest.mark.parametrize('args',read_yaml())
    def test01_api(self,args):
        print(args)
        dates = args['api_request']
        method = dates['method']
        url = dates['url']
        headers = dates['headers']
        params = dates['params']
        print(method)
        if method == 'get':
            print(111)
            json_json = requests.get(url,params=params,headers=headers)
            print(json_json.json())
        elif method == 'post':
            print(222)
        else:
            print(3333)


if __name__ == '__main__':
    pytest.main(['-s','test_homepage.py'])
