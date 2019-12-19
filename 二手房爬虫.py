#coding=utf-8
'''
仅仅爬取了前100页的数据
为了避免反爬虫策略，设定每5秒钟抓取一页信息
@time = 2019-12-03
@author = rs
'''

from bs4 import BeautifulSoup
import re
import csv
import requests
import pandas as pd
from random import choice
import time

'''
最新发布:
第一页:https://bj.lianjia.com/ershoufang/co32/
第二页:https://bj.lianjia.com/ershoufang/pg2co32/
...
第100页:https://bj.lianjia.com/ershoufang/pg100co32/
'''
base_url1 = 'https://bj.lianjia.com/ershoufang/pg'
base_url2 = 'co32/'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 BIDUBrowser/8.7 Safari/537.36'}




columns = ['小区', '地区', '厅','平米数','方向','状态','层','build-year','形式','钱','单位','网址','推荐语']
# 如果文件由第一行,就不用了
with open('链家新房100个.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow(columns)
    file.close()
i=1
for j in range(100):
    urll = base_url1+ str(i) +base_url2
    print(urll)
    i += 1
    get_page=requests.get(urll)
    bs_page = BeautifulSoup(get_page.text, 'html.parser')
    list_house = bs_page.findAll('div', class_='info clear')
    for house_one in list_house:
        
        house_info    = house_one.find_all('div', class_='houseInfo')
        position_info = house_one.find_all('div', class_='positionInfo')
        totalPrice    = house_one.find_all('div', class_='totalPrice')
        href          = house_one.find_all('div', class_='title')

        # 正则提取
        # 小区名,位置
        position_str  =re.findall('_blank">(.+)</a.+_blank">(.+)?</a', str(position_info))
        position_str1 =list(position_str[0])
        # print(type(position_str1),position_str1)

        # 房子信息
        house_info_str=re.findall('span>(.+)?</div>', str(house_info))
        house_info_str = str(house_info_str)[2:-2].split('|')
        # print(type(house_info_str), house_info_str)


        totalPrice_str=re.findall('<span>(.+)</span>(.+)</div>', str(totalPrice))
        totalPrice_str = list(totalPrice_str[0])
        # print(type(totalPrice_str), totalPrice_str)
        
        
        href_str      =re.findall('http.+html', str(href))
        # print(type(href_str), href_str)
        
        AD_str = re.findall('_blank">(.+)?</a>', str(href))
        # print(type(AD_str), AD_str)
        
        house_all = position_str1 + house_info_str + totalPrice_str + href_str + AD_str
        
        print(house_all)
        
        # writer.writerow()
        with open('链家新房100个.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(house_all)
            file.close()
        
    print(f'---第{i}页---')
    times = choice([3, 4, 5, 6])
    print(f'sleep{times}\n')
    time.sleep(times)
print('fin')
