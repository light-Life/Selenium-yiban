# !/usr/bin/python
# -*- coding:utf-8 -*-
# time: 2020.3.5
import requests,re,json,os,time
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0'}
def First_page(url):
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
        number = 1
        soup = BeautifulSoup(response.text,'lxml')#这里不能直接给url因为BeautifulSoup不支持直接打开链接
        #第一次解析（class为photo-item所有元素）
        for First_analysis in soup.find_all(attrs={'class':'photo-item'}):
            One_analysis = str(First_analysis)
            #写入文件（方便对照）
            '''
            with open('对照.txt','a') as f:
                f.write(One_analysis)
            '''
            # 提取内容地址
            address = First_analysis.a.attrs['href']
            # 提取网页名
            name = First_analysis.a.attrs['title']

            print(number,'\t\033[35m正在提取:', name, '\033[0m')
            number = number + 1
            yield address,name#目前只能想到在循环条件下只能用yield方式返回数据

#对地址内容进行解析提取
def Analysis_address(html):
    for content in html:
        Website = 'https:'+content[0]#requests不能识别没加https的url
        seid = re.sub('\D','',Website)#提取up主的id
        id = 'https://api.vc.bilibili.com/link_draw/v1/doc/detail?doc_id='+seid
        response = requests.get(id,headers=headers)

        if response.status_code == 200:
            data_str = str(response.text)#转化成str类型
            data_json = json.loads(data_str)#继续转化为json格式
            data = data_json['data']#切出data的内容
            item = data['item']#切出item的内容

            for pictures in item['pictures']:#切出data的内容并遍历出来
                img_src = pictures['img_src']#现在就可以切出图片地址了
                name = os.path.split(img_src)[1]#os.path是获取文件属性的意思spliot是指指定区分符进行切片
                response = requests.get(img_src)
                '''                        
                有点麻烦，但实在想不到其他方法，百度都点爆了有木有啊QAQ  5555~~
                只怪这网站是动态渲染的并且的嵌套实在是太多了，幸好代码少还没有验证式反爬虫，再多一点就不得了了
                目前可以肯定的是通过嵌套遍历的方式无法提取出信息，未来看看能有什么其他方法
                '''
                yield response,name

#保存图片
def Preservation(picture):
    for Return in picture:
        chart = Return[0]#切出图片
        name = Return[1]#切出标题

        if os.path.exists('E:/哔哩哔哩jk小姐姐') == True:  # 判断是否这个文件，有则直接写入，无则创建了再写入
            with open('E:/哔哩哔哩jk小姐姐/%s'+name, 'wb') as f:
                f.write(chart.content)
        else:
            print('正在E盘创建文件夹')
            os.mkdir('E:/哔哩哔哩jk小姐姐')#创建目录/文件
            with open('E:/哔哩哔哩jk小姐姐/%s'+name, 'wb') as f:
                f.write(chart.content)

if __name__=='__main__':
    for x in range(1,51):
        a = str(x)#需要转化为str形式
        url = 'https://search.bilibili.com/photo?keyword=jk&page='+a
        html = First_page(url)
        picture = Analysis_address(html)
        Preservation(picture)
        print('\n\t\t\033[36m>>>>>提取完一页了哦<<<<<\033[0m\n')

print('\n\n\033[32m提取完成！！！\033[0m')



