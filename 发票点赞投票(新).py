import base64
import random
import requests
import threading
import time
def yiban_check_ma(cookie):#请求验证码
    yiban_check_ma_headers = {"Accept": "application/json, text/javascript, */*; q=0.01", "Accept-Encoding": "gzip, deflate, br","Accept-Language": "zh-CN,zh;q=0.9", "Connection": "close","Content-Type": "application/x-www-form-urlencoded; charset=UTF-8","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ""(KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",'Cookie': cookie}
    yiban_check_ma_url = "https://www.yiban.cn/captcha/index?Mon Dec 14 2020 18:45:34 GMT 0800 (中国标准时间)="
    try:
        yiban_check_ma_r = requests.get(yiban_check_ma_url,headers=yiban_check_ma_headers,timeout=None)
    except Exception:
        yiban_check_ma_r = requests.get(yiban_check_ma_url, headers=yiban_check_ma_headers,timeout=None)
    image_data = base64.b64encode(yiban_check_ma_r.content).decode().replace("\r", "")
    baidu_api_headers = {'Content-Type':'application/x-www-form-urlencoded'}#必选参数
    baidu_api_data = {'image':image_data.encode("utf8")} #base64编码的图片,已去头
    try:
        baidu_api_r = requests.post(url='https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=24.cae65f3935c6094515f0fa9b948e28c4.2592000.1617352274.282335-22957927',headers=baidu_api_headers, data=baidu_api_data,timeout=None)
    except Exception:
        baidu_api_r = requests.post(url='https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=24.cae65f3935c6094515f0fa9b948e28c4.2592000.1617352274.282335-22957927',headers=baidu_api_headers, data=baidu_api_data,timeout=None)
    if 'words_result' in baidu_api_r.json() and len(baidu_api_r.json()['words_result']) >= 1 and len(baidu_api_r.json()['words_result'][0]['words']) == 1:
        yzm = baidu_api_r.json()['words_result'][0]['words']
        toupiao(cookie,yzm)
    else:
        yiban_check_ma(cookie)
def toupiao(cookie,yzm):
    shiju = ['一寸光阴一寸金，寸金难买寸光阴。', '明日复明日，明日何其多，我生待明日，万事成蹉跎。', '天行健，君子以自强不息。', '少壮不努力，老大徒悲伤。', '三更灯火五更鸡，正是男儿读书时。','黑发不知勤学早，白首方悔读书迟。', '宝剑锋从磨砺出，梅花香自苦寒来。']
    x = shiju[random.randint(0, 6)]
    toupiao_headers = {'Accept': 'application/json, text/javascript, */*; q=0.01','Accept-Encoding': 'gzip, deflate','Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ru;q=0.5,zh-TW;q=0.4,da;q=0.3,ht;q=0.2,tr;q=0.1','Connection': 'keep-alive','Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8','Cookie': cookie,'DNT': '1','Host': 'www.yiban.cn','Origin': 'http://www.yiban.cn','Referer': 'http://www.yiban.cn/my/publishvote','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51','X-Requested-With': 'XMLHttpRequest'}
    toupiao_data = {'puid': '***', 'scope_ids': '***', 'title': x, 'subjectTxt': '','subjectPic': '', 'options_num': '2', 'scopeMin': '1', 'scopeMax': '1', 'minimum': '1','voteValue': '2023-09-31 23:59', 'voteKey': '2', 'public_type': '0', 'isAnonymous': '1','voteIsCaptcha': '0', 'istop': '1', 'sysnotice': '2', 'isshare': '1', 'rsa': '1','dom': '.js-submit', 'group_id': '1000680', 'subjectTxt_1': shiju[random.randint(0, 6)],'subjectTxt_2': shiju[random.randint(0, 6)], 'captcha': yzm}
    #改三个参数puid、scope_ids、group_id#学院id
    toupiao_r = requests.post(url='https://www.yiban.cn/vote/vote/add', headers=toupiao_headers, data=toupiao_data,timeout=None)
    if '200' in toupiao_r.text:
        print(toupiao_r.status_code,toupiao_r.json()['message'])
        #点赞
        print('投票ID:',toupiao_r.json()['data']['lastInsetId'])
        vote_id = toupiao_r.json()['data']['lastInsetId']
        DianZan_datas = {
            'puid': '***',
            'group_id': '***',
            'vote_id': vote_id,
            'actor_id': '***',
            'flag': '1'
        }
        DianZan_r = requests.post(url='https://www.yiban.cn/vote/vote/editLove',headers=toupiao_headers,data=DianZan_datas)
        # 点赞调试代码
        if DianZan_r.json()['message'] == '操作成功':
            print('点赞成功')
        else:
            print(DianZan_r.json())
        #投票
        TouTiao_data = {
            'puid':'***',
            'group_id':'***',
            'vote_id':vote_id,
            'actor_id':'***',
            'voptions_id':'***',
            'minimum':'1',
            'scopeMax':'1'
        }
        TouTiao_r = requests.post(url='https://www.yiban.cn/vote/vote/act',headers=toupiao_headers,data=TouTiao_data)
        #投票调试代码
        if TouTiao_r.json()['message']=='操作成功':
            print('投票成功')
        else:
            print(TouTiao_r.json())
    else:
        print(toupiao_r.status_code,toupiao_r.json())
        yiban_check_ma(cookie)
cookie = '***'
for i in range(0,100):
    yiban_check_ma(cookie)
    time.sleep(60)
