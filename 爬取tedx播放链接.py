import re
from urllib.request import urlopen
from bs4 import BeautifulSoup

url='https://v.youku.com/v_show/id_XNjcwMDM5NjE2.html?spm=a2hbt.13141534.1_2.d1_2'

html = urlopen(url)
bsobj = BeautifulSoup(html.read(), "html.parser")
txt_title='YOUK_TEDX_LINK'
f= open(txt_title+".txt", "a+")
# 仅找到名字
# namelist_1=bsobj.find_all('div',{'class':'pic-text-item'})
# for name in namelist_1:
#     print(name.text)

# 找到链接
namelist_1=bsobj.find_all('div',{'class':'pic-text-item'})
num=1

for name in namelist_1:
    linklist=re.findall('http.+html',str(name))
    title=name.text
    for link in linklist:
        num +=1
        print(title,link)
        f.write(f'{title}:{link}\n')  # 这句话自带文件关闭功能，不需要再写f.close()

f.close()
