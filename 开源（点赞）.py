# !/usr/bin/python
# -*- coding:utf-8 -*-
# name: huayang
# time: 2020.11.11

import re
import time
import requests
import threading
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

url = '***'#总投票界面

def First(x,y,cookie,cookie2,name):
    browser = webdriver.Chrome()
    for x in range(int(x),int(y)):#页
        urls = url + str(x)
        headers = {
            'Connection': 'close', 'Accept': 'application/json, text/javascript, */*; q=0.01', 'DNT': '1',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Origin': 'https://www.yiban.cn',
            'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://www.yiban.cn/my/publishvote', 'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ru;q=0.5,zh-TW;q=0.4,da;q=0.3,ht;q=0.2,tr;q=0.1',
            'Cookie': cookie
        }
        try:
            response = requests.get(urls,headers=headers)
        except Exception:
            response = requests.get(urls, headers=headers)
        span = re.findall('.*?<span class="tx">(.*?)</sp.*?',response.text,re.S)
        href = re.findall('.*?target="_blank" href="(.*?)"',str(span))
        for i in href:
            i = 'https://www.yiban.cn' + i
            browser.get(i)
            browser.add_cookie({'name': 'yiban_user_token', 'value': cookie2})
            time.sleep(0.5)
            browser.refresh()
            time.sleep(0.5)
            source = browser.page_source
            if '取消赞' in source:
                print('已点赞')
            else:
                location = browser.find_element_by_id('btn_like')#必须使用id才能定位鼠标悬停
                ActionChains(browser).move_to_element(location).perform()#鼠标悬停
                time.sleep(0.1)
                browser.find_element_by_id('btn_like').click()  # 点赞
                time.sleep(0.5)
            if 'id="vote_result" style=' in source:
                print('已投票')
            else:
                browser.find_element_by_class_name('btn_chs').click()  # 选择
                time.sleep(0.4)
                browser.find_element_by_class_name('btn_vote').click()  # 投票按钮
            if name in source:
                print('已评论')
            else:
                speech = browser.find_element_by_xpath('//input[@type="text"]')
                speech.send_keys('大家好，我是马保国')#评论
                time.sleep(0.3)
                try:
                    browser.find_element_by_class_name('submit').click()  # 发送评论
                except:
                    browser.find_element_by_class_name('submit').click()  # 发送评论
                time.sleep(0.5)
    print('循环结束')

cookie = [
    'name','cookie!',
    '**','***!',
    '**','***!',
    '**','***!',
    '**','***!',
    '**','***!'

]#第一个是真实姓名，二是此cookie值
if __name__ == '__main__':
    threads = []    #创建线程数组
    number = 1 #cookie
    number2 = 0#cookie2
    number3 = 0#name
    for i in range(6):#设置线程数，cookie要记得随之更改
        cookie2 = re.findall('.*?yiban_user_token=(.*?)!.*?', str(cookie), re.S)#cookie最后加上!在不影响cookie的同时能使正则匹配成功
        threads.append(threading.Thread(target=First, args=(111,120,cookie[number],cookie2[number2],cookie[number3])))#页数改前两位
        number +=2
        number2 +=1
        number3 +=2
    for t in threads:
            t.start()   #启动线程
    for t in threads:
            t.join()    #守护线程
'''
本代码优势：
1.可以刷共建指数
2.完全模拟真人点击防封率大大提升
3.采用多线程刷分效率大大提高
4.代码简洁有注释
'''