import requests # 调用requests库
from bs4 import BeautifulSoup # 调用BeautifulSoup库
res = requests.get('https://wordpress-edu-3autumn.localprod.oc.forchange.cn/all-about-the-future_04/#comment-18168')
# 返回一个response对象，赋值给res
html = res.text
# 把res的内容以字符串的形式返回
soup = BeautifulSoup( html,'html.parser') 
# soup = BeautifulSoup(res.text,'html.parser') #另一种写法
# 把网页解析为BeautifulSoup对象
items = soup.find_all(class_="comment-body") # 每一个评论的块
# print(items)
for item in items:#太多了，爬前30看看
    # print(item)
    # print('$$$$$$$$$$$$$$$$$$$')
    who = item.find(class_="comment-author vcard") #找到水评论的
    time = item.find("time") #评论的时间
    brief = item.find(class_="comment-content") #在评论的主体内容
    # print(who ,'\n',time,'\n',brief) # 打印提取出的数据
    # print(type(who),'\n',type(time),'\n',type(brief)) # 打印提取出的数据类型
    #print('··············') #想与上边的区分开
    print(who.text)
    # print(time.text)
    print(time['datetime'])
    print(brief.text)
    print('================================')
    #print(' ')
    #print(items)
