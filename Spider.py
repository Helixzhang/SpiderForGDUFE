import time
import requests
from PIL import Image
from io import BytesIO
from lxml import etree

class Spider(object):
    """
    爬虫大类
    """
    def __init__(self, username: str,password: str):
        """
        初始化,登陆
        """
        self.headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75'}
        self.login(username,password)

    def login(self, username,password):
        """
        POST模拟登陆
        """
        res = requests.get(url='http://jwxt.gdufe.edu.cn/jsxsd/',headers=self.headers)
        for key in res.cookies.get_dict().keys():
            cookie = key+"="+res.cookies.get_dict()[key]+";"

        self.headers['Cookie'] = cookie
        res = requests.get(url='http://jwxt.gdufe.edu.cn/jsxsd/verifycode.servlet',headers=self.headers)
        image = Image.open(BytesIO(res.content))
        image.show()

        randomcode = input('请输入刚才显示的验证码:')
        login_data = {
            'USERNAME':username,
            'PASSWORD':password,
            'RANDOMCODE':randomcode
        }
        requests.post(url='http://jwxt.gdufe.edu.cn/jsxsd/xk/LoginToXkLdap',headers=self.headers,params=login_data)

    def reqClass(self,term_id:str='2020-2021-2',weeks:int=16):
        """
        爬取课程表,并保存为csv文件
        """
        f = open('class.csv','w',encoding='utf-8')
        f.truncate()
        for week in range(1,weeks+1):
            
            data = {'xnxq01id': term_id,'zc':week}
            response = requests.post(url='http://jwxt.gdufe.edu.cn/jsxsd/xskb/xskb_list.do',headers=self.headers,params=data)
            tree = etree.HTML(response.text)
            index = 0

            for div in tree.xpath('//*[@class="kbcontent"]'):
                if div.xpath('.//text()') != ['\xa0']:
                    day = (index%7)+1
                    num = int(index/7)+1
                    lst=[x.replace(',','、') for x in div.xpath('.//text()')]
                    _class = "{},{},{},".format(week,day,num)+",".join(lst)
                    print(_class)
                    f.write(_class+'\n')
                index+=1
            
            time.sleep(5)
