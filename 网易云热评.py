# !/usr/bin/pythoy
# -*- coding:utf-8 -*-
# time: 2020.4.8
# item_name: 爬取网易云热评
# Effect: 爬取网易云歌单里的：歌名，id，封面地址，用户，评论，评论数，评论时间，获赞数


import requests,re,time

url = 'https://music.163.com/weapi/v6/playlist/detail?csrf_token=eb3780ee25e0c1437b81941daa994e75'
headers = {
   'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
   'Origin':'http://music.163.com',
   'Host':'music.163.com'
}
#加密（核心）
data = {
   'params': 'ZYaoHCPhsVg52paJnoU/RuYbVYM1YVPfwChWkeoOnl9Hqje/nZApFZP1KCbolAa5TxtoROCZPe7eZWxV'
             'QSKSBCNp3yD8qLtIwyqfOjMHUH42nmbKh6twU2V75j0Am9MYVONWERXP7IEGbwuBAg+1uKVU9oYe8+0/'
             '4XQ6a27zB5lKrgZVB2qQHDhNb0852q79rg3qBOPd8heOiacu+gFbgzJMvSyrMeVvwHxTOgYU6VM=',
   'encSecKey': '6bb3665d4067b3a2faf4109a8674fa6769c83c5bcc4821d8f6a2ee852d40b6f5bc0370937869'
                '420ac267304c9d60b078392e3a1e3caf105d9488d19bcb1411823c70532b36394f4ec4f440518'
                '1864c1b76d7a2172e1142c57b581eb4c679cc6ac17b811d749611a00c66079e9aadd24aa387a61'
                'd96747e444b11116ac60af072'
}


def post():
    response = requests.post(url,headers=headers,data=data)
    if response.status_code == 200:
        return response.text
    return None


def song_sheet():
    indes = re.findall('.*?{"name":"(.*?)","id":(.*?),.*?"picUrl":"(.*?)",',post(),re.S)
    for inde in indes:
        name = inde[0]#歌名
        id = inde[1]
        cover = inde[2]#封面
        url = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_' + id +'?csrf_token=2c79f81074588cf33c669f682d8131cf'
        response = requests.post(url,headers=headers,data=data)
        if response.status_code == 200:
            hotComments = re.findall('hotComments":(.*?),"code".*?',response.text,re.S)#提出热评
            total_comment = re.findall('.*?"total":(.*?),.*?',response.text,re.S)#所有评论数
            total_comments = re.sub('\D', '', str(total_comment))#去除多余的符号
            hotComments_str = str(hotComments)
            contents = re.findall('.*?nickname":"(.*?)",.*?content":"(.*?)".*?time":(.*?),"likedCount":(.*?),.*?',hotComments_str,re.S)
            for content in contents:
                user = content[0]#用户名
                comment = content[1]#评论
                times = content[2]
                fabulous = content[3]#赞
                print(name,'\t\t评论：',total_comments,'\n')

                #转换为标准时间
                timeNum = int(times)#必须要把str转化成int类型
                timeTemp = float(timeNum / 1000)
                tupTime = time.localtime(timeTemp)
                stadardTime = time.strftime("%Y-%m-%d %H:%M:%S", tupTime)#标准时间
                yield name,cover,user,comment,stadardTime,fabulous,total_comments


#保存
def Preservation():
    for dictionaries in song_sheet():
        name = dictionaries[0]#歌名
        cover = dictionaries[1]#封面地址
        user = dictionaries[2]#用户
        commment = dictionaries[3]#评论
        stadardTime = dictionaries[4]#时间
        fabulous = dictionaries[5]#赞
        total_comment = dictionaries[6]#所有评论

        with open('网易云音乐.txt','a', encoding='utf-8') as f:
            f.write('歌曲：'+str(name)+'\n')
            f.write('评论总数：' + str(total_comment) + '\n')
            f.write('封面：'+str(cover)+'\n')
            f.write('用户：'+str(user)+'\n')
            f.write('评论：'+str(commment)+'\n')
            f.write('时间：'+str(stadardTime)+'\t\t')
            f.write('赞：'+str(fabulous)+'\n')
            f.write('========================'+'\n')

if __name__ == '__main__':
    Preservation()
    print('\n\n\t\t提取完成')

    '''
    就这样吧，有兴趣的朋友可以做得更美观，比如同一首歌只循环评论、用户、时间、赞，
    这样写貌似有点麻烦，还可以把回复的评论去掉等等......
    共计耗时81.26s,所以封ip是不可能的。文件大小为1.37M
    '''
