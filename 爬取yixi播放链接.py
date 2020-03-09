import re
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup

url='http://i.youku.com/i/UNDg0NTA2OTY0/videos?spm=a2hzp.8253869.0.0&order=1&page='

txt_title='YOUKU_YIXI_LINK'
f= open(txt_title+".txt", "a+")

# 目前17页
for i in range(1,18):
    html = urlopen(url+str(i))
    bsobj = BeautifulSoup(html.read(), "html.parser")
    # 找到链接
    namelist_1=bsobj.find_all('div',{'class':'v va'})
    for name in namelist_1:
        # 正则找title
        title=re.findall('alt=+(.+)src',str(name))

        # bs找link
        links=name.find_all('div',{'class':'v-link'})
        link=re.findall('href="(.+html)',str(links))

        # 转换字符串
        titlestr=title[0]
        linkstr='https:' + link[0]

        # 打印保存
        print(titlestr,linkstr)
        f.write(f'{titlestr}:{linkstr}\n')  # 这句话自带文件关闭功能，不需要再写f.close()
    time.sleep(1)

f.close()
