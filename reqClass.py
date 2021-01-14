import time
import requests
from PIL import Image
from io import BytesIO
from lxml import etree
headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5',
'Content-Type': 'application/x-www-form-urlencoded',
'Cookie': '',
'Host': 'jwxt.gdufe.edu.cn',
'Origin': 'http://jwxt.gdufe.edu.cn',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75'}

f = open('class.csv','w',encoding='utf-8')
f.truncate()
for i in range(1,17):
    
    data = {'xnxq01id': '2020-2021-2','zc':i}
    response = requests.post(url='http://jwxt.gdufe.edu.cn/jsxsd/xskb/xskb_list.do',headers=headers,params=data)
    tree = etree.HTML(response.text)
    index = 0

    for tr in tree.xpath('//*[@class="kbcontent"]'):
        if tr.xpath('.//text()') != ['\xa0']:
            day = (index%7)+1
            num = int(index/7)+1
            lst=[]
            for stri in tr.xpath('.//text()'):
                lst.append(stri.replace(',','、'))
            _class = "{},{},{},".format(i,day,num)+",".join(lst)
            print(_class)
            f.write(_class+'\n')
        index+=1
    
    time.sleep(5)


