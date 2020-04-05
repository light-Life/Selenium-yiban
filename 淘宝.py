# !/usr/bin/python
# -*- coding:utf-8 -*-
# time: 2020.4.3
import requests,re,time,json


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
    'cookie':'？？？',
}
name = input('请输入要分析的商品名称：')
print('请输入查看方式A,B,C (A:综合,B:销量(从高到低),C:信用)')
See = input()
if See == 'A':
    url = 'https://s.taobao.com/search?q=' + name
    response = requests.get(url, headers=headers)
elif See == 'B':
    url = 'https://s.taobao.com/search?q=' + name + '&sort=sale-desc'
    response = requests.get(url, headers=headers)
elif See == 'C':
    url = 'https://s.taobao.com/search?q=' + name + '&sort=credit-desc'
    response = requests.get(url, headers=headers)
else:
    print('输入格式不正确,请重新输入')

def parse():

    Price = re.findall(r'\"view_price\"\:\"[\d\.]*\"', response.text)  # findall搜索全部字符串，viex_price是源代码中表价格的值，后面的字符串为数字和点组成的字符串
    detailed = re.findall(r'\"raw_title\"\:\".*?\"', response.text)  # 找到该字符串和后面符合正则表达式的字符串

    for i in range(len(detailed)):
        Prices = eval(Price[i].split(':')[1])  # re.split() 将一个字符串按照正则表达式匹配结果进行分割，返回列表类型
        detaileds = eval(detailed[i].split(':')[1])  # 将re获得的字符串以：为界限分为两个字符串,并取第二个字符串
        print(Prices,'\t',detaileds)

parse()
