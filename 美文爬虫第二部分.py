import csv, threading, requests, json, re
import random
import multiprocessing,time


from urllib import request
from bs4 import BeautifulSoup
from pymysql import *


# 请求头
user_agent_list = [ \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]
UserAgent = random.choice(user_agent_list)

# cookie换成自己的
headers = {
    'User-Agent': UserAgent,
}



# 创建Mysql的 connection连接,passowrd换成自己的
conn = connect(host='localhost', port=3306, database='meiwen', user='root', password='112212', charset='utf8')
# 获取cursor对象
cs1 = conn.cursor()

table_name="duanpian"




def run(n):

    """第二+第三部分"""
    time.sleep(random.randint(5,10)/10)
    print("当前抓取:",n)
    index_num=n
    try:
        """为了拿到两个链接"""
        sqls = f'select url from {table_name} where index_num=%s;'
        values = (index_num)
        cs1.execute(sqls, values)
        url_s = cs1.fetchone()
        print("print(url_s):",url_s)
        # conn.commit()
        try:
            """每个问题帖子下的回答写入数据库"""
            getcontent(index_num,contenturl=url_s )
        except Exception as e:
            print(e)
            print(index_num, '没有写得评论数据 NO_OK!!!!!!!!!')
        finally:
            pass
    except Exception as e:
        print(e)
    print('结束')




def getcontent(index_num, contenturl, ):
    """爬取评论的函数"""
    url = contenturl[0]

    # 发送请求，并把响应内容赋值到变量res里面
    res = requests.get(url=url, headers=headers, )
    print(res.status_code)
    # 如果响应成功，继续
    if int(res.status_code) == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        # print(soup)
        block = soup.findAll('div',class_="content")
        # print(type(block))
        # print(block)
        contenttext=''
        for item in block:
            plist= item.find_all('p')[0:-9]
            for one in plist:
                pargone=one.text
                contenttext =contenttext+pargone+"\n"
        print(contenttext)
        sqls = f'UPDATE {table_name} set content=%s where index_num=%s;'
        values = (contenttext,index_num)
        cs1.execute(sqls, values)
        conn.commit()
        print('content存完', index_num)

        # time.sleep(0.55)

    time.sleep(0.55)






if __name__ == '__main__':
    Nums = []
    sqls = f'select index_num from {table_name} where content is NULL;'
    # values = (index_num)
    cs1.execute(sqls)
    url_s = cs1.fetchall()
    for ones in url_s:
        Nums.append(int(ones[0]))
    print(Nums)
    print(len(Nums))
    start = time.time()
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    # pool = multiprocessing.Pool(1)
    print('电脑核数:',multiprocessing.cpu_count())
    pool.map(run, Nums)
    pool.close()
    pool.join()
    print(time.time() - start)

