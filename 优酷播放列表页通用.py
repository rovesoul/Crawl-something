import re
from urllib.request import urlopen
from bs4 import BeautifulSoup

url='https://v.youku.com/v_show/id_XNDAwNzk5NzEzNg==.html?spm=a2h0k.11417342.soresults.dposter'
#白岩松 'https://v.youku.com/v_show/id_XMzk5NTk2OTA2MA==.html?spm=a2hcb.12492884.m_15187_c_53830.d_4&s=fbd3d1aa2cb0427b8bf5&scm=20140719.rcmd.15187.show_fbd3d1aa2cb0427b8bf5'
# 观复嘟嘟 'https://v.youku.com/v_show/id_XMjk3Mjc0NjEzNg==.html?spm=a2hcb.12492884.m_4580_c_11250_1.d_6&s=5eefbfbd40db817a11ef&scm=20140719.rcmd.4580.show_5eefbfbd40db817a11ef'
# 逻辑思维 'https://v.youku.com/v_show/id_XNDAwNzk5NzEzNg==.html?spm=a2h0k.11417342.soresults.dposter'

html = urlopen(url)
bsobj = BeautifulSoup(html.read(), "html.parser")
txt_title='逻辑思维经典'
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
