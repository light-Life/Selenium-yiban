# !/usr/bin/python
# -*- coding:utf-8 -*-
# time: 2020.4.3
import requests,re,time,json


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
    'cookie':'t=5d46c6f11441ec6a4366e7c763991c2b; cna=7tINFyZCtDwCAXWtoWMv04Sg; thw=cn; sgcookie=EhUeSi9ylDvek%2Bx7HldBM; uc3=lg2=Vq8l%2BKCLz3%2F65A%3D%3D&nk2=F5RDLees1AKpIN8%3D&id2=UUphyu%2BNKdBeuJjc0A%3D%3D&vt3=F8dBxdAW67nZDEPcaw8%3D; lgc=tb612384282; uc4=nk4=0%40FY4I7jVTE0Jq8nRfiwBcewhm9S%2Fibw%3D%3D&id4=0%40U2grEanMlotI7fXroTjqMcb0jH1vsI%2BF; tracknick=tb612384282; _cc_=URm48syIZQ%3D%3D; tfstk=cNfFB0wsvWFUGSTF9IAyRk2RnNpdZM_hrf8XKt5A6MtQOM9hilnJ5_xk7U6dqpf..; mt=ci=11_1; _m_h5_tk=348957540247e59ed9653cfc0fa484d0_1585915407125; _m_h5_tk_enc=2fcb07673db87e8192493148691ff251; enc=z4CsPUcQRYEx5zRY4qL2znrzYicC6Bzyp5WTVtkn%2Bis0EyqQt4cLjtB7K9IKZbw1jnzUZTC7NU65t7h%2FLmQSeSUwwf1WJ2K6iqZSWar37yk%3D; hng=CN%7Czh-CN%7CCNY%7C156; v=0; cookie2=1e1cfca10f65faeb6f519f770cf7fc7b; _tb_token_=f5435e3361ee6; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; uc1=cookie14=UoTUP2uQrqu4lw%3D%3D; JSESSIONID=96145A8E1F1CF1F6401A6B2C859A3D88; isg=BG1tOOjNz0Sj2asnHcG_nBHkfAnnyqGcP1Zi9K9yqYRzJo3YdxqxbLv0EPrAvblU; l=dBN3VzZ4QXrrEJOzBOCaCAJLdlbOSIRYYu8NJQtXi_5aL6T_ya7Oo1Qv7F96VjWf93TB4lOf6Tv9-etkZQDmndK-g3fPaxDc.',
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