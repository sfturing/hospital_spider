import requests
from bs4 import BeautifulSoup
import pymysql.cursors
config = {
          'host':'127.0.0.1',
          'port':3306,
          'user':'root',
          'password':'root',
          'db':'hosdb',
          'charset':'utf8',
          'cursorclass':pymysql.cursors.DictCursor,
          }
connection = pymysql.connect(**config)
curs = connection.cursor()
sql = 'INSERT INTO doctor (docotor_name,doctor_sex,hospital_name,offices_name,doctor_img,doctor_title,teach_title,doctor_administrative,doctor_degree,doctor_forte,doctor_about) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'}
URL = '''http://yyk.99.com.cn/tianjin/'''
r = requests.get(URL, headers=headers, timeout=500)
beaytifuleSoup = BeautifulSoup(r.text, "lxml")
tabListDiv = beaytifuleSoup.find_all("div",class_ = "tablist")
i = 0
for area in  tabListDiv:
    hospital = area.find_all("li")
    for h_name in hospital:
        if h_name.text !="":
            url = h_name.a.get("href")
            detailUrl = url + "zhuanjia.html"
            #解析医院的医生连接
            detail_soup = BeautifulSoup(requests.get(detailUrl).text, "lxml")
            hpdoc_table_div = detail_soup.find_all("table", class_="hpdoc_table")
            for hpdoc_table_info in hpdoc_table_div:
                docotor_class = hpdoc_table_info.find_all("td", class_="tdr")
                for docotor_info in docotor_class:
                    if docotor_info.text !="医生":
                        docotor_url = docotor_info.a.get("href")
                        #得到医生的详细介绍
                        ins_url = docotor_url[:23]+"/introduction"+docotor_url[23:]
                        doc_soup = BeautifulSoup(requests.get(ins_url).text, "lxml")
                        try:
                            doc_img = doc_soup.find("div", class_ = "s-infor-tp")
                            doctor_img = str(doc_img.find("img").get("src"))
                        except:
                            doctor_img= str("http://ysk.99.com.cn/images/ysk_nopicture.jpg")
                        docotorCommom_div =doc_soup.find("div", class_ = "s-infor-txt")
                        docotor_cominfo = docotorCommom_div.find_all("dd")
                        docotor_list = []
                        for common_info in docotor_cominfo:
                            docotor_list.append(common_info.text.strip())
                        try:
                           docotor_name = docotor_list[0]
                        except:
                            docotor_name ="暂无相关信息"
                        try:
                           doctor_sex = docotor_list[1]
                        except:
                            doctor_sex ="暂无相关信息"
                        try:
                           hospital_name = docotor_list[2]
                        except:
                            hospital_name ="暂无相关信息"
                        try:
                           offices_name = docotor_list[3]
                        except:
                            offices_name ="暂无相关信息"
                        try:
                           doctor_title = docotor_list[4]
                        except:
                            doctor_title ="暂无相关信息"
                        title_div = doc_soup.find("div", "pro-cont")
                        doctor_forte=str(title_div.find("td", "pro-tab-txt3").text.strip())
                        title_list =[]
                        for titile_info in title_div.find_all("td", "pro-tab-txt2"):
                            title_list.append(titile_info.text.strip())
                        try:
                           teach_title = title_list[0]
                        except:
                            teach_title ="暂无相关信息"
                        try:
                           doctor_administrative = title_list[1]
                        except:
                            doctor_administrative ="暂无相关信息"
                        try:
                           doctor_degree = title_list[2]
                        except:
                            doctor_degree ="暂无相关信息"
                        try:
                            doctor_about = str(doc_soup.find("div", "pro-doct-cont").text.strip())
                        except:
                            doctor_about = "暂无相关信息"
                        print(doctor_about)
                        curs.execute(sql, (docotor_name,doctor_sex,hospital_name,offices_name,doctor_img,doctor_title,teach_title,doctor_administrative,doctor_degree,doctor_forte,doctor_about))
                        connection.commit()
                        i = i+1
                        print(i)
                        hon_info = []
                        common_info = []
connection.close()
