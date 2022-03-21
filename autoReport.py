# -*- coding: utf8 -*-
import requests
import json
import time, datetime
import random

# 需要自动填报的账号密码
userInfo = [
    {'username': 'XXXXXX', 'password': 'XXXXXXX'},
#     如果需要多个账号填写，依次添加即可
#   {'username': 'XXXXXX', 'password': 'XXXXXXX'},
#   {'username': 'XXXXXX', 'password': 'XXXXXXX'}
]


def main_handler(event, context):
    resultText = ''
    for i in range(len(userInfo)):
        waitTime = random.randint(10, 300)
        # 每次提交时随机等待10~300秒，可使每天不是在同一个时间点填写
        time.sleep(waitTime)
        report_user = automatic(userInfo[i]['username'], userInfo[i]['password'])
        resultText += str(userInfo[i]['username']) + str(report_user) + '   '
    return (resultText)


def automatic(username, password):
    r = requests.session()
    r.headers = {
        "Referer": "https://app.upc.edu.cn/uc/wap/login?redirect=https%3A%2F%2Fapp.upc.edu.cn%2Fncov%2Fwap%2Fdefault%2Findex",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
    }
    r.get("https://app.upc.edu.cn/uc/wap/login?redirect=https%3A%2F%2Fapp.upc.edu.cn%2Fncov%2Fwap%2Fdefault%2Findex")

    a = eval(
        r.post("https://app.upc.edu.cn/uc/wap/login/check", data={"username": username, "password": password}).text)

    if (len(a['m']) != 4):
        return "login error"
    t = None
    t = r.get("https://app.upc.edu.cn/ncov/wap/default/index").json()
    i = t['d']['oldInfo']
    # print( t['d'])
    i['date'] = t['d']['info']['date']
    i['id'] = t['d']['info']['id']
    i['created'] = t['d']['info']['created']
    # print(i)
    its = r.post("https://app.upc.edu.cn/ncov/wap/default/save", data=i).json()
    return its["m"]