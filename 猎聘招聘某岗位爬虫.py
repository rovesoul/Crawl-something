'''
1: https://www.liepin.com/zhaopin/?init=-1&headckid=fb8c04cf13f4395e&fromSearchBtn=2&ckid=fb8c04cf13f4395e&degradeFlag=0&sfrom=click-pc_homepage-centre_searchbox-search_new&key=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90&siTag=ZFDYQyfloRvvhTxLnVV_Qg%7EfA9rXquZc5IkJpXC-Ycixw&d_sfrom=search_fp&d_ckId=aa0171e4a826756be831908d340eca9b&d_curPage=99&d_pageSize=40&d_headId=aa0171e4a826756be831908d340eca9b&curPage=0
2: https://www.liepin.com/zhaopin/?init=-1&headckid=fb8c04cf13f4395e&fromSearchBtn=2&ckid=fb8c04cf13f4395e&degradeFlag=0&sfrom=click-pc_homepage-centre_searchbox-search_new&key=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90&siTag=ZFDYQyfloRvvhTxLnVV_Qg%7EfA9rXquZc5IkJpXC-Ycixw&d_sfrom=search_fp&d_ckId=aa0171e4a826756be831908d340eca9b&d_curPage=3&d_pageSize=40&d_headId=aa0171e4a826756be831908d340eca9b&curPage=1
3: https://www.liepin.com/zhaopin/?init=-1&headckid=fb8c04cf13f4395e&fromSearchBtn=2&ckid=fb8c04cf13f4395e&degradeFlag=0&sfrom=click-pc_homepage-centre_searchbox-search_new&key=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90&siTag=ZFDYQyfloRvvhTxLnVV_Qg%7EfA9rXquZc5IkJpXC-Ycixw&d_sfrom=search_fp&d_ckId=aa0171e4a826756be831908d340eca9b&d_curPage=2&d_pageSize=40&d_headId=aa0171e4a826756be831908d340eca9b&curPage=1
4: https://www.liepin.com/zhaopin/?init=-1&headckid=fb8c04cf13f4395e&fromSearchBtn=2&ckid=fb8c04cf13f4395e&degradeFlag=0&sfrom=click-pc_homepage-centre_searchbox-search_new&key=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90&siTag=ZFDYQyfloRvvhTxLnVV_Qg%7EfA9rXquZc5IkJpXC-Ycixw&d_sfrom=search_fp&d_ckId=aa0171e4a826756be831908d340eca9b&d_curPage=2&d_pageSize=40&d_headId=aa0171e4a826756be831908d340eca9b&curPage=3
'''
# 导入模块
from bs4 import BeautifulSoup
import re
import csv
import requests
import pandas as pd
from random import choice
import time

url_base = 'https://www.liepin.com/zhaopin/?init=-1&headckid=fb8c04cf13f4395e&fromSearchBtn=2&ckid=fb8c04cf13f4395e&degradeFlag=0&sfrom=click-pc_homepage-centre_searchbox-search_new&key=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90&siTag=ZFDYQyfloRvvhTxLnVV_Qg%7EfA9rXquZc5IkJpXC-Ycixw&d_sfrom=search_fp&d_ckId=aa0171e4a826756be831908d340eca9b&d_curPage=1&d_pageSize=40&d_headId=aa0171e4a826756be831908d340eca9b&curPage='

title=['发布日期','岗位名称','薪酬','工作城市','学历','工作年限','公司名称','公司行业','其他方面','链接']
csvpath='/Users/donghuibiao/网课学习/自己想做的项目/爬取智联招聘/智联招聘.csv'
urltitle='https://www.liepin.com'
# 创建csv部分
with open(csvpath, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow(title)
    file.close()

i=0

for j in range(100):
    url=url_base+str(i)
    print(url)
    i+=1
    get_page = requests.get(url)
    bs_page = BeautifulSoup(get_page.text, 'html.parser')
    list_jobs = bs_page.findAll('div', class_='sojob-item-main clearfix')
    for job in list_jobs:
        # print(job)

        date = str(job.find_all('p', class_='time-info clearfix'))[45:56]
        print('date-------',date)
        job_name = job.find_all('div', class_='job-info')
        job_name = str(re.findall('<h3 title="(.*)">?', str(job_name)))[2:-2]
        print('job-name-------',job_name)
        wage = job.find_all('p', class_='condition clearfix')
        wage = str(re.findall('<span class="text-warning">(.*)</span>?', str(wage)))[2:-2]
        print('wage-------', wage)
        city = job.find_all('a', class_='area')
        city = str(re.findall('">(.*)</a>?', str(city)))[2:-2]
        print('city-------', city)
        education = job.find_all('span', class_='edu')
        education = str(re.findall('class="edu">(.*)</span>?', str(education)))[2:-2]
        print('edu-------', education)
        workyear = job.find_all('p', class_='condition clearfix')
        workyear = str(re.findall('<span>(.*)</span>?', str(workyear)))[2:-2]
        print('workyear-------', workyear)
        company_name = job.find_all(target='_blank')
        company_name = str(re.findall('title=".*>(.*)</a>?', str(company_name)))[2:-2]
        print('company-name-------', company_name)
        company_cycle = str(job.find_all('p', class_='field-financing')).replace('\n','').replace(' ','')
        company_cycle = ''.join(list(re.findall("[^\'\"0-9a-z %\$\&  # @\*;-_-=<->/\[\]\s]", str(company_cycle))))
        print(company_cycle)
        others = job.find_all('p', class_='temptation clearfix')
        others = list(re.findall('<span>(.*)</span>', str(others)))
        others =('|'.join(others))
        print(others)
        lin_url = job.find_all('div', class_='job-info')
        lin_url = str(re.findall('href="(.*shtml)"?', str(lin_url)))[2:-2]
        if lin_url[0:2] == '/a':
            lin_url = urltitle + lin_url
        print(lin_url)

        print(f'第{j+1}页--------------------------------------------------')

        joball=[date,job_name,wage,city,education,workyear,company_name,company_cycle,others,lin_url]
        with open(csvpath, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(joball)
            

file.close()
print('fin')
