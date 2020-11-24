# !/usr/bin/python
# -*- coding:utf-8 -*-
# name: Qsj377
# time: 2020.11.9

import requests,base64,random,time,threading
def renzheng(cookie):
    renzheng_r = requests.get(url='http://www.yiban.cn/user/info/index?type=2',headers={
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ru;q=0.5,zh-TW;q=0.4,da;q=0.3,ht;q=0.2,tr;q=0.1',
        'Cookie': cookie
    })
def yiban_check_ma(cookie):#请求验证码
    yiban_check_ma_headers = {"Accept": "application/json, text/javascript, */*; q=0.01", "Accept-Encoding": "gzip, deflate, br","Accept-Language": "zh-CN,zh;q=0.9", "Connection": "close","Content-Type": "application/x-www-form-urlencoded; charset=UTF-8","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ""(KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",'Cookie': cookie}
    yiban_check_ma_url = "https://www.yiban.cn/captcha/index?Tue%20Dec%2004%202018%2000:01:26%20GMT+0800%20(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)"
    try:
        yiban_check_ma_r = requests.get(yiban_check_ma_url,headers=yiban_check_ma_headers,timeout=3)
    except Exception:
        yiban_check_ma_r = requests.get(yiban_check_ma_url, headers=yiban_check_ma_headers, timeout=None)
    image_data = base64.b64encode(yiban_check_ma_r.content).decode().replace("\r", "")
    baidu_api(image_data,cookie)
def baidu_api(image_data,cookie):#需要传入字符串:image_data
    baidu_api_headers = {'Content-Type':'application/x-www-form-urlencoded'}#必选参数
    baidu_api_data = {'image':image_data.encode("utf8")} #base64编码的图片,已去头
    try:
        baidu_api_r = requests.post(url='https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=24.f3f0f5de06299de7a2a22a4c29dbc0b9.2592000.1608696091.282335-22957927',headers=baidu_api_headers, data=baidu_api_data,timeout=3)
    except Exception:
        baidu_api_r = requests.post(url='https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=24.f3f0f5de06299de7a2a22a4c29dbc0b9.2592000.1608696091.282335-22957927',headers=baidu_api_headers, data=baidu_api_data, timeout=None)
    if('words_result' in baidu_api_r.json() and len(baidu_api_r.json()['words_result'])>=1):
        yzm = baidu_api_r.json()['words_result'][0]['words']
        toupiao(cookie,yzm)
    else:
        yiban_check_ma(cookie)
def toupiao(cookie,yzm):
    shiju = ['一寸光阴一寸金，寸金难买寸光阴。', '明日复明日，明日何其多，我生待明日，万事成蹉跎。', '天行健，君子以自强不息。', '少壮不努力，老大徒悲伤。', '三更灯火五更鸡，正是男儿读书时。','黑发不知勤学早，白首方悔读书迟。', '宝剑锋从磨砺出，梅花香自苦寒来。']
    x = shiju[random.randint(0, 6)]
    toupiao_headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ru;q=0.5,zh-TW;q=0.4,da;q=0.3,ht;q=0.2,tr;q=0.1',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': cookie,
        'DNT': '1',
        'Host': 'www.yiban.cn',
        'Origin': 'http://www.yiban.cn',
        'Referer': 'http://www.yiban.cn/my/publishvote',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51',
        'X-Requested-With': 'XMLHttpRequest'
    }
    toupiao_data = {'puid': '12792328', 'scope_ids': '1000680', 'title': x, 'subjectTxt': '','subjectPic': '', 'options_num': '2', 'scopeMin': '1', 'scopeMax': '1', 'minimum': '1','voteValue': '2021-06-17 21:55', 'voteKey': '2', 'public_type': '0', 'isAnonymous': '1','voteIsCaptcha': '0', 'istop': '1', 'sysnotice': '2', 'isshare': '1', 'rsa': '1','dom': '.js-submit', 'group_id': '1000680', 'subjectTxt_1': shiju[random.randint(0, 6)],'subjectTxt_2': shiju[random.randint(0, 6)], 'captcha': yzm}
    #改三个参数puid#忘了、scope_ids#忘了、group_id#学院id
    try:
        toupiao_r = requests.post(url='https://www.yiban.cn/vote/vote/add', headers=toupiao_headers, data=toupiao_data,timeout=3)
    except Exception:
        toupiao_r = requests.post(url='https://www.yiban.cn/vote/vote/add', headers=toupiao_headers,data=toupiao_data, timeout=None)
    print(toupiao_r.json())
    if('444' in toupiao_r.text):
        renzheng(cookie)
        toupiao(cookie,yzm)
    elif ('200' in toupiao_r.text):
        print(toupiao_r.json()['message'],x)
    else:
        yiban_check_ma(cookie)


#print(requests.get('https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=***_secret=***').json()['access_token'])
cookie = '***'+str(int(round(time.time(),3)*1000))#在这里填写cookie
for i in range(0,10000):
    yiban_check_ma(cookie)





