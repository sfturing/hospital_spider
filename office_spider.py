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
sql='INSERT INTO offices (offices_name,hospital_name,doctor_num,offices_honor,offices_equipment,offices_about,offices_diagnosis_scope) VALUES(%s,%s,%s,%s,%s,%s,%s)'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'}
URL = '''http://yyk.99.com.cn/sanjia/tianjin/'''
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
            #解析医院的科室连接
            detail_soup = BeautifulSoup(requests.get(detailUrl).text, "lxml")
            hpdoc_table_div = detail_soup.find_all("table", class_="hpdoc_table")
            for hpdoc_table_info in hpdoc_table_div:
                office_class = hpdoc_table_info.find_all("td", class_="tdl")
                for office_info in office_class:
                    if office_info.text !="科室":
                        office_url = office_info.a.get("href")
                        #得到科室的详细介绍
                        ins_url = office_url[:23]+"/introduction"+office_url[23:]
                        office_soup = BeautifulSoup(requests.get(ins_url).text, "lxml")
                        common_div = office_soup.find_all("table", class_="pr-h-tab")
                        #将科室的基本信息存入list
                        common_list = []
                        for common_info in common_div:
                            common_listinfo = common_info.find_all("font")
                            for common in common_listinfo:
                                common_list.append(common.text)
                            try:
                                offices_name = common_list[0]
                            except:
                                offices_name = "暂无相关信息"
                            try:
                                hospital_name = common_list[1]
                            except:
                                hospital_name = "暂无相关信息"
                            try:
                                doctor_num = common_list[2]
                            except:
                                doctor_num = "暂无相关信息"
                            try:
                                offices_equipment = common_list[4]
                            except:
                                offices_equipment = "暂无相关信息"
                        about_div = office_soup.find_all("div", class_="pr-in-cont")
                        for about_info in about_div:
                            offices_about = str(about_info.p)
                        diagnosis_div = office_soup.find_all("div", class_="pr-ra-cont")
                        for diagnosis_info in diagnosis_div:
                            offices_diagnosis_scope = str(diagnosis_info.p)
                        hon_div = office_soup.find_all("div", class_="pr-hon-cont")
                        hon_list = []
                        for hon_info in hon_div:
                            for honor in hon_info.find_all("p"):
                                hon_list.append(str(honor))
                        try:
                            offices_honor = hon_list[1]
                        except:
                            offices_honor = "暂无相关信息"
                        #print(type(offices_name), type(hospital_name), type(doctor_num), type(offices_honor), type(offices_equipment), type(offices_about), type(offices_diagnosis_scope))
                        curs.execute(sql, (offices_name, hospital_name, doctor_num, offices_honor, offices_equipment, offices_about, offices_diagnosis_scope))
                        connection.commit()
                        i = i+1
                        print(i)
                        hon_info = []
                        common_info = []
connection.close()








