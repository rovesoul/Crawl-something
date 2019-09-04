import requests, random, bs4
from bs4 import BeautifulSoup
#第一页：https://movie.douban.com/top250?start=0&filter=
#第二页：https://movie.douban.com/top250?start=25&filter=
j=1
file_movie = open('风变-爬虫课-豆瓣电影.txt','w',encoding='utf-8')#w意思是写入；a的意思是append
for i in range(1,11):
    print(i)#识别一下第几页爬到的
    file_movie.write('第'+str(i)+'页\n')
    URL='https://movie.douban.com/top250?start='+str((i-1)*25)+'&filter='
    res_page = requests.get(URL)#获得URL数据
    bs_page = BeautifulSoup(res_page.text,'html.parser')# 解析数据
    list_movies = bs_page.find_all('div',class_="item")# 查找最小父级标签class="item"
    for movie in list_movies:
        print('——————————————第',str(j),'部好电影\n')
        file_movie.writelines('——————————————第'+str(j)+'部好电影\n')
        # print('电影名字是：')
        # file_movie.writelines('电影名字是：\n')
        names=movie.find_all('span',class_="title")
        for name in names:
            print(name.text)
            file_movie.writelines(name.text+'\n')
        nameothers=movie.find_all('span',class_="other")
        for nameother in nameothers:
            print(nameother.text)
            file_movie.writelines(nameother.text+'\n')
        daoyan=movie.find('div',class_="bd")#导演
        print(daoyan.p.text[29:-25])#打印导演部分，不要下边其他
        file_movie.writelines(daoyan.p.text[29:-25]+'\n')
        score=movie.find('span',class_="rating_num")#评分
        print('评分：'+score.text)#打印评分
        says=movie.find('span',class_="inq")
        try:
            print('推荐语：'+says.text)
            file_movie.write('推荐语：'+says.text + '\n')
        except:AttributeError
        file_movie.writelines('评分：'+score.text+'\n')
        weburl=movie.find('a')#抓链接
        print(weburl['href'])#打印链接
        file_movie.writelines('网址详情'+weburl['href']+'\n\n\n\n')
        print('  ')
        j=j+1
    # print(list_movie)
    print('=======================================================')#区分一下一页page爬完了 
file_movie.close()