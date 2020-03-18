# !/usr/bin/python
# -*- coding:utf-8 -*-
#time: 2020.3.7
import requests,re,os,time
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0'}
def chart():
    print('\n请输入要提取图片的网址:')
    url = input()
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')#用BeautifulSoup+lxml解析器解析内容
        for position in soup.find_all(attrs={'property': 'og:image'}):#切出并遍历property：og:image所有结果
            position_str = str(position)#结果转化成str形式
            position_list = re.findall('<meta.*?content="(.*?)".*?>', position_str)#用正则匹配出无用的留下地址
            position_str = str(position_list[0])#再将list形式转换成str形式并最终切出图片地址
            position_rq = requests.get(position_str)  #最后将str转换成requests.models.Response形式
            name = os.path.split(position_str)[1] #切出文件名
            if os.path.exists('c:/img') == True:
                print('\n正在写入文件\t>>>>>>>>>>>>>>>>>>>>>')
                with open('c:/img/%s' + name, 'wb') as f:  # 以字符串的形式写入
                    f.write(position_rq.content)  # 只接受requests形式
            else:
                print('\n在C盘创建img的文件夹')
                os.mkdir('c:/img')
                print('\n正在写入文件\t>>>>>>>>>>>>>>>>>>>>>')
                with open('c:/img/%s' + name, 'wb') as f:  # 以字符串的形式写入
                    f.write(position_rq.content)  # 只接受requests形式
            print('\n文件已保存\tC:/img')

chart()
number = 1
while number > 0:
    print('\n是否继续获取\t(y/n):')
    information = input()
    if information == 'y':
        chart()
    elif information == 'n':
        print('\n记得下次再来哦QAQ\t(3s后将自动关闭窗口...)')
        time.sleep(3)
        break
    else:
        print('\n格式错误，请重新输入:')

