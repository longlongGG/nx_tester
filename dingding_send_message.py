#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Dragon
# @Software: PyCharm
import json
import requests
import sys

def send_msg(msg):
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    url = 'https://oapi.dingtalk.com/robot/send?access_token=09761c8d49dcb69019d7735b13b7c59209756add5ee15eb42cbbdf489ee6974d'
    data = {
        "msgtype": "text",
        "at": {
            #"atMobiles": reminders,
            "isAtAll": False,
        },
        "text": {
            "content": msg,
        }
    }
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return r.text


# if __name__ == '__main__':
#     msg = "这只是一个测试"
#     #reminders = ['15055667788']  # 特殊提醒要查看的人,就是@某人一下
#     print(send_msg(msg))