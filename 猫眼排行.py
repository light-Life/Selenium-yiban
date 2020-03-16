import requests
import re  # 正则
import xlwt  # excel

def 第一页(url):
    headers = {'User-Agent': 'Mozilla/5.0'}  # 伪装头
    response = requests.get(url, headers=headers)  # 加上伪装头请求
    if response.status_code == 200:
        return response.text  # 返回字符串
    return  # 否，则返回None


def 解析第一页(html):
    print('\033[31m正在写入>>>>>>>>>>>>>>>>\033[0m')
    # 匹配正则表达式
    pattern = re.compile(  # 将正则字符串编译成正则表达式
        '<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name">.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>',
        re.S
    )
    items = re.findall(pattern, html)  # 结果录入字典 findall:搜索整个字符串，然后返回匹配表达式的所有内容
    for item in items:
        yield {  # 当作是return
            '排名': item[0],  # 切片
            '图片地址': item[1],
            '电影名': item[2],
            '主演': item[3].strip()[3:],  # 移除字符串头尾指定的字符（默认为空格或换行符）或字符序列
            '上映时间': item[4].strip()[5:],
            '评分': item[5] + item[6]
        }


def main(offset):
    url = 'https://maoyan.com/board/4?offset=' + str(offset)
    html = 第一页(url)
    for item in 解析第一页(html):
        xr = str(item)
        print('\033[35m排名:\033[0m', item.get('排名'), '\033[35m电影名:\033[0m', item.get('电影名'), '\033[35m主演:\033[0m',
              item.get('主演'), '\033[35m名称:\033[0m', item.get('名称'), '\033[35m时间:\033[0m', item.get('时间'),
              '\033[35m图片地址:\033[0m', item.get('图片地址'), '\033[35m评分:\033[0m', item.get('评分'))
        排名 = str(item.get('排名'))
        电影名 = str(item.get('电影名'))
        主演 = str(item.get('主演'))
        上映时间 = str(item.get('上映时间'))
        图片地址 = str(item.get('图片地址'))
        评分 = str(item.get('评分'))
        with open('猫眼.txt', 'a') as a:  # a随便取
            a.write(xr+'\n')
        global x  # 定义一个去全局变量
        # 写入
        worksheet.write(x, 0, 排名)
        worksheet.write(x, 1, 电影名)
        worksheet.write(x, 2, 主演)
        worksheet.write(x, 3, 上映时间)
        worksheet.write(x, 4, 图片地址)
        worksheet.write(x, 5, 评分)
        x = x + 1


if __name__ == '__main__':  # 当模块被直接运行时，if...以下代码块将被运行，当模块是被导入时，代码块不被运行
    workbook = xlwt.Workbook(encoding='utf-8')  # 工作簿
    worksheet = workbook.add_sheet('猫眼数据')  # 工作表
    x = 1
    for i in range(10):
        main(offset=i * 10)

    # 设置单元格的宽度
    worksheet.col(1).width = 270 * 20
    worksheet.col(2).width = 650 * 20
    worksheet.col(3).width = 280 * 20
    worksheet.col(4).width = 1200 * 20
    # 创建颜色
    pattern = xlwt.Pattern()  # 创建模式对象Create the Pattern
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN  # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
    pattern.pattern_fore_colour = 5  # 设置模式颜色 May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes on...
    style = xlwt.XFStyle()  # 创建样式对象Create the Pattern
    style.pattern = pattern  # 将模式加入到样式对象Add Pattern to Style
    # 写入数据
    worksheet.write(0, 0, '排名', style)
    worksheet.write(0, 1, '电影名', style)
    worksheet.write(0, 2, '主演', style)
    worksheet.write(0, 3, '开映时间', style)
    worksheet.write(0, 4, '图片地址', style)
    worksheet.write(0, 5, '评分', style)
    # 保存文件
    workbook.save('猫眼电影TOP100.xls')
print('\n\n\033[32m写入完成.............\033[0m')
