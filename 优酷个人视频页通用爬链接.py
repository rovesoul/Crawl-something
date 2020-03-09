import re
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup

url='https://i.youku.com/i/UNzE4OTQ2OTU1Ng==/videos?spm=a2hzp.8253869.0.0&order=1&page='

txt_title='10分钟系列'
f= open(txt_title+".txt", "a+")

# 空字典
list_self={}
# 目前多少页
num=4
for i in range(1,num+1):
    print(f'第{i}启动')
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

        # 转换字符串并存入字典
        titlestr=title[0]
        linkstr='https:' + link[0]
        list_self[titlestr]=linkstr
    time.sleep(1)
    print(f'第{i}结束\n')

# 重新排序
list_sort=sorted(list_self.items(),key=lambda x:x[0])
for list_one in list_sort:
    print(list_one[0],list_one[1])
    # 打印保存
    f.write(f'{list_one[0]}:{list_one[1]}\n')  # 这句话自带文件关闭功能，不需要再写f.close()
f.close()
