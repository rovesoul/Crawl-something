import requests # 引用requests库
from bs4 import BeautifulSoup # 引用BeautifulSoup库
res_foods = requests.get('http://www.xiachufang.com/explore/')# 获取数据
bs_foods = BeautifulSoup(res_foods.text,'html.parser')# 解析数据
#print(bs_foods)# 打印解析结果,暂时隐去

list_foods = bs_foods.find_all('div',class_='info pure-u')
# 查找最小父级标签
# print(list_foods)#暂时隐藏，打印最小父级标签
menus=[]
i=1
for food in list_foods:
    menu=[]
    name=food.find('a') 
    nametrue=name.text[17:-13]#17是切掉前边的空格，-13是切掉后边的空格加换行符
    # print(name.text[17:])#17是把空格错过去
    # print('http://www.xiachufang.com'+name['href'])
    weburl='http://www.xiachufang.com'+name['href']
    yuansu=food.find(class_="ing ellipsis") 
    yuansus=yuansu.text[1:-1]#1和-1是切掉头尾的换行符号
    # print(yuansu.text)
    menus.append([i,nametrue,weburl,yuansus])#注意多个元素添加，小括号里要有中括号
    i=i+1

print('fin')
print(menus)
