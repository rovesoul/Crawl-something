import requests, random, bs4  ,re , time ,csv
from bs4 import BeautifulSoup

    
data_url= "https://3g.dxy.cn/newh5/view/pneumonia_peopleapp"
f_path  = "./data/data.csv"
sf_path = "./data/data-sum.csv"



times_str=""
# 抓总数
def get_sums():
    # 获取上次时间
    with open(sf_path, 'r', newline='', encoding='utf8') as f:
        rcsv = csv.reader(f)
        for rows in rcsv:
            late_time = rows[-1]
        f.close()
    

    
    res_page = requests.get(data_url)  # 获得URL数据
    res_page.encoding = 'utf-8'
    bs_page = BeautifulSoup(res_page.text, 'html.parser')  # 解析数据
    # print(bs_page)
    # 获取时间戳
    time_data = bs_page.find_all(
        'p', class_="mapTitle___2QtRg")  # 查找最小父级标签class="item"
    time_str = time_data[0].text
    time_num = re.findall("截至 (.+?) 数据统计", time_str)
    time_num = time_num[0]
    times = time.strftime(
        '%Y-%m-%d %H:%M', time.strptime(time_num, "%Y-%m-%d %H:%M"))
    # print(times)
    times_str = str(times)
    if times_str != late_time:

        # 获取数据方面
        sum_data = bs_page.find_all(
            'span', class_="content___2hIPS")  # 查找最小父级标签class="item"
        for data in sum_data:
            heads = {"确诊": 0, "疑似": 0,
                        "治愈": 0, "死亡": 0, "更新日期": ""}
            area_msg = data.text
            area_msg = area_msg.replace(" ", "")
            print(area_msg)
            recon_num = re.findall("确诊{1}(\d*)", area_msg)
            spy_num = re.findall("疑似{1}(\d*)", area_msg)
            cure_num = re.findall("治愈{1}(\d*)", area_msg)
            deth_num = re.findall("死亡{1}(\d*)", area_msg)
            try:
                heads['确诊'] = recon_num[0]
            except Exception as e:
                pass
            try:
                heads['疑似'] = spy_num[0]
            except Exception as e:
                pass
            try:
                heads['治愈'] = cure_num[0]
            except Exception as e:
                pass
            try:
                heads['死亡'] = deth_num[0]
            except Exception as e:
                pass
            try:
                heads['更新日期'] = times
            except Exception as e:
                pass
            # print(recon_num, spy_num, cure_num, deth_num,times)
            # print(area_msg)
            # print(heads)

            # 写入数据
            # file_path 是 csv 文件存储的路径

            with open(sf_path, 'a', newline='', encoding='utf8') as f:
                w = csv.writer(f, delimiter=',')
                w.writerow(list(heads.values()))
        return times_str, "★★★★★总数已更新"
    else:
        return times_str, "◇◇◇◇◇总数没有更新"



# 抓各地的
def get_heads():

    # 获取上次时间
    with open(f_path, 'r', newline='', encoding='utf8') as f:
        rcsv = csv.reader(f)
        for rows in rcsv:
            late_time = rows[-1]
        f.close()
    
    
    
    res_page = requests.get(data_url)#获得URL数据
    res_page.encoding='utf-8'
    bs_page = BeautifulSoup(res_page.text,'html.parser')# 解析数据
    # 获取时间戳
    time_data = bs_page.find_all('p',class_="mapTitle___2QtRg")# 查找最小父级标签class="item"
    time_str= time_data[0].text
    time_num = re.findall("截至 (.+?) 数据统计", time_str)
    time_num = time_num[0]
    times = time.strftime('%Y-%m-%d %H:%M',time.strptime(time_num, "%Y-%m-%d %H:%M"))
    # print(times)
    times_str = str(times)
    if times_str !=late_time:

        # 获取数据方面
        list_data = bs_page.find_all('div',class_="descBox___3dfIo")# 查找最小父级标签class="item"
        for data in list_data:
            names = data.find_all('p', class_="descList___3iOuI")
            for name in names:
                heads={"城市":"","确诊":0,"疑似":0,"治愈":0,"死亡":0,"更新日期":""}
                area_msg=name.text
                city = area_msg.split(" ")[0]
                heads["城市"]=city
                print(city)
                
                area_msg=area_msg.replace(" ","")
                recon_num = re.findall("确诊{1}(\d*)", area_msg)
                spy_num = re.findall("疑似{1}(\d*)", area_msg)
                cure_num = re.findall("治愈{1}(\d*)", area_msg)
                deth_num = re.findall("死亡{1}(\d*)", area_msg)

                try:
                    heads['确诊'] = recon_num[0]
                except Exception as e:
                    pass
                try:
                    heads['疑似'] = spy_num[0]
                except Exception as e:
                    pass
                try:
                    heads['治愈'] = cure_num[0]
                except Exception as e:
                    pass
                try:
                    heads['死亡'] = deth_num[0]
                except Exception as e:
                    pass
                try:
                    heads['更新日期'] = times
                except Exception as e:
                    pass
                # print(recon_num, spy_num, cure_num, deth_num,times)
                # print(area_msg)
                print(heads)

                # 写入数据
                # file_path 是 csv 文件存储的路径
                
                with open(f_path, 'a', newline='', encoding='utf8') as f:
                    w = csv.writer(f, delimiter=',')
                    w.writerow(list(heads.values()))
                    
                    

                print("\n")
        return times_str, "★★★★★各省数据已更新"
    else:
        return times_str, "◇◇◇◇◇各省没有更新"
    

while True:
    a =get_heads()
    b = get_sums()
    print(a,"fin")
    print(b),'fin'
    time.sleep(600) #10分钟一更新


