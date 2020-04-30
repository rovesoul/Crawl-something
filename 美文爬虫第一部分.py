import time
import random

from pymysql import *
import csv
import requests
from bs4 import BeautifulSoup


# 请求头
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
url = 'https://www.zhihu.com/api/v4/topics/19614893/feeds/timeline_question?'

fullxpath= "/html/body/div[6]/div[1]/div[4]/ul/li[2]/h2/a"
url1="http://www.ruiwen.com/jingdianmeiwen/"
url2="http://www.ruiwen.com/jingdianmeiwen/list_2.html"
url3="http://www.ruiwen.com/jingdianmeiwen/list_3.html"
url_duanpian="http://www.ruiwen.com/xiaoshuo/"

maxpage=20
# 设置offset的起始值为第一页的值：0,最大16829
offset = 0
Maxoffset = 16829

# 创建connection连接
conn = connect(host='localhost', port=3306, database='meiwen', user='root',password='111222', charset='utf8')
# 获取cursor对象
cs1 = conn.cursor()

# 存mysql函数
def save_sql(sqls,values):
    cs1.execute(sqls, values)
    conn.commit()

# 爬列表页面函数
def clap_meiwen():
    global offset
    index_num = 1
    for anum in range(maxpage+1):
        print(f'目前正在爬第 {anum} 页')
        url_clap="http://www.ruiwen.com/xiaoshuo/list_"+str(anum)+".html"
        # 封装参数
        params = {
            'include': 'data[?(target.type=topic_sticky_module)].target.data[?(target.type=answer)].target.content,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;data[?(target.type=topic_sticky_module)].target.data[?(target.type=answer)].target.is_normal,comment_count,voteup_count,content,relevant_info,excerpt.author.badge[?(type=best_answerer)].topics;data[?(target.type=topic_sticky_module)].target.data[?(target.type=article)].target.content,voteup_count,comment_count,voting,author.badge[?(type=best_answerer)].topics;data[?(target.type=topic_sticky_module)].target.data[?(target.type=people)].target.answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics;data[?(target.type=answer)].target.annotation_detail,content,hermes_label,is_labeled,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;data[?(target.type=answer)].target.author.badge[?(type=best_answerer)].topics;data[?(target.type=article)].target.annotation_detail,content,hermes_label,is_labeled,author.badge[?(type=best_answerer)].topics;data[?(target.type=question)].target.annotation_detail,comment_count;',
            'offset': str(offset),
            'limit': '10',
        }
        # 发送请求，并把响应内容赋值到变量res里面
        res = requests.get(url_clap, headers=headers)
        # 确认这个response对象状态正确
        print(res.status_code)

        # 如果响应成功，继续
        if int(res.status_code) == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            # print(soup)
            block = soup.findAll('h2')
            # print("block:",block)
            try:
                for item in block:
                    try:
                        title = [i.get('title') for i in item.find_all('a', {'title': True})][0]
                        hrefs = [i.get('href') for i in item.find_all('a', {'href': True})][0]
                        hrefs = "http://www.ruiwen.com"+hrefs
                        print(title, hrefs)
                        sqls = 'INSERT INTO duanpian (url,title) VALUES (%s,%s);'
                        values = (hrefs, title)
                        save_sql(sqls, values)

                    except:pass
            except :pass
        print("保存ok")
        time.sleep(random.randint(2, 4) / 10)



clap_meiwen()
# 关闭cursor对象
cs1.close()
# 关闭connection对象
conn.close()
