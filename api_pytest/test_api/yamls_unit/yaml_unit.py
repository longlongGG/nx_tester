#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Dragon
# @Software: PyCharm
#读取yaml文件
import yaml

def read_yaml():
    with open('../yamls/homepage.yaml', 'r', encoding='utf-8') as f :
        data = yaml.load(f,Loader=yaml.FullLoader)
        return data
