import requests
from lxml import etree
import time
import threading
def First(cookie):
    for i in range(2208, 3456):
        url = 'http://www.yiban.cn/Newgroup/showMorePub/group_id/***/puid/***/type/3/page/' + str(i)
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9','Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6','Cache-Control': 'max-age=0', 'Connection': 'close', 'Cookie': cookie, 'DNT': '1', 'Host': 'www.yiban.cn','Upgrade-Insecure-Requests': '1','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.81'}
        r = requests.get(url=url, headers=headers)
        link = etree.HTML(r.content).xpath('/html/body/main/div/div/div/div[1]/section[2]/ul//li/div/div[1]/span[1]/a/@href')
        for j in range(0, len(link)):
            link[j] = 'https://www.yiban.cn' + link[j]
            # 点赞
            vote_id = link[j][50:59]
            DianZan_datas = {'puid': '12792328', 'group_id': '1000680', 'vote_id': vote_id, 'actor_id': '32628138','flag': '1'}
            DianZan_r = requests.post(url='https://www.yiban.cn/vote/vote/editLove', headers=headers,data=DianZan_datas)
            # 点赞调试代码
            if DianZan_r.json()['message'] == '操作成功':
                pass
            # print('点赞成功')
            else:
                pass
            # print(DianZan_r.json())
            time.sleep(0.1)
            # 投票
            TouTiao_data = {'puid': '***', 'group_id': '***', 'vote_id': vote_id, 'actor_id': '32628138','voptions_id': '441568499', 'minimum': '1', 'scopeMax': '1'}
            TouTiao_r = requests.post(url='https://www.yiban.cn/vote/vote/act', headers=headers, data=TouTiao_data)
            # 投票调试代码
            if TouTiao_r.json()['message'] == '操作成功':
                pass
            # print('投票成功')
            else:
                pass
            # print(TouTiao_r.json())
            time.sleep(0.2)
        print(i, '页', etree.HTML(requests.get(url=url, headers=headers).content).xpath('/html/body/main/div/div/div/div[1]/section[1]/div[2]/div/span[1]/text()'))
cookie = (
    '***'
)
threads = []
for i in cookie:
    threads.append(threading.Thread(target=First, args=(i, )))
for t in threads:
    t.start()
    time.sleep(0.2)
for t in threads:
    t.join()
