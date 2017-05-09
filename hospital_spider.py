import requests
from bs4 import BeautifulSoup
import pymysql.cursors
import  time
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
sql='INSERT INTO hospital (hospital_name,hospital_area,hospital_img,hospital_dean_name,hospital_year,hospital_nature,hospital_grade,hospital_offices_num,medical_insurance_num,hospital_bed_num,outpatient_num,is_medical_insurance,hospital_equipment,hospital_about,hospital_honor,hospital_url,hospital_phone,hospital_address,hospital_post_code,hospital_bus_route) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'}
URL = '''http://yyk.99.com.cn/sanjia/shanghai/'''
r = requests.get(URL, headers=headers, timeout=500)
beaytifuleSoup = BeautifulSoup(r.text, "lxml")
tabListDiv = beaytifuleSoup.find_all("div",class_ = "tablist")
i = 0
for area in  tabListDiv:
    hospital = area.find_all("li")
    for h_name in hospital:
        if h_name.text !="":
            url = h_name.a.get("href")
            detailUrl = url + "jianjie.html"
            detail_soup = BeautifulSoup(requests.get(detailUrl).text, "lxml")
            hos_name = detail_soup.find_all("div", class_= "hospital_name clearbox")
            for name in hos_name:
                hospital_name = name.h1.text.strip()
            hos_img = detail_soup.find_all("div", class_ = "hpi_img")

            for eveImg in hos_img:
                    if eveImg.a.get("href")[0]=="/":
                        img_url = "http://yyk.99.com.cn" + eveImg.a.get("href")
                    else:
                        img_url = eveImg.a.get("href")
            hospital_img =img_url

            hos_info = detail_soup.find_all("div", class_="leftpad10 hpbasicinfo")
            for eveInfo in hos_info:
                info_tab = eveInfo.find_all("td", class_ = "tdr")
                info_list = []
                for txt in info_tab:
                    value = txt.text.strip()
                    if "-" in value:
                        value ="0"
                    info_list.append(value)
                hospital_area = info_list[1]
                hospital_dean_name = info_list[2]
                hospital_year = info_list[3]
                hospital_nature = info_list[4]
                hospital_grade = info_list[5]
                hospital_offices_num = int(info_list[6])
                medical_insurance_num = int(info_list[7])
                hospital_bed_num = int(info_list[8])
                outpatient_num = int(info_list[9])
                is_medical_insurance = info_list[10]
            about = detail_soup.find_all("div",class_ = "hpcontent")
            about_info = []
            for eve_about in about:
                if eve_about != "":
                    about_info.append(eve_about.text.strip())
            try:
                hospital_equipment = about_info[0]
            except:
                hospital_equipment = "此处没有简介"
            try:
                hospital_about = about_info[1]
            except:
                hospital_about = "此处没有简介"
            try:
                hospital_honor = about_info[2]
            except:
                hospital_honor = "此处没有简介"

            hos_connect = detail_soup.find_all("div", class_ = "leftpad10 contact")
            conn_info = []
            #print(hos_connect)
            for eveInfo in  hos_connect:
                info_tab = eveInfo.find_all("td", class_ = "tdr")
                bus_route = eveInfo.find("td", class_ = "lasttdr lasttd")
                hospital_bus_route = bus_route.text.strip()
                for connVlue in info_tab:
                    conn_info.append(connVlue.text.strip())
                hospital_url = conn_info[0]
                hospital_phone = conn_info[1]
                hospital_post_code = conn_info[len(conn_info)-1]
                hospital_address = conn_info[len(conn_info)-2]
            curs.execute(sql, (hospital_name,hospital_area,hospital_img,hospital_dean_name,hospital_year,hospital_nature,hospital_grade,hospital_offices_num,medical_insurance_num,hospital_bed_num,outpatient_num,is_medical_insurance,hospital_equipment,hospital_about,hospital_honor,hospital_url,hospital_phone,hospital_address,hospital_post_code,hospital_bus_route))
            connection.commit()
            info_list = []
            about_info =[]
            conn_info = []
            i=i+1
            print(i)

connection.close()




