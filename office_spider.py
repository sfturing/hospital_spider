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
sql="INSERT INTO offices (offices_name,hospital_name,doctor_num,offices_honor,offices_equipment,offices_about,offices_diagnosis_scope) VALUES(%s,%s,%s,%s,%s,%s,%s)"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'}
URL = '''http://yyk.99.com.cn/sanjia/tianjin/'''
r = requests.get(URL, headers=headers, timeout=500)
beaytifuleSoup = BeautifulSoup(r.text, "lxml")
tabListDiv = beaytifuleSoup.find_all("div",class_ = "tablist")
for area in  tabListDiv:
    hospital = area.find_all("li")
    for h_name in hospital:
        if h_name.text !="":
            url = h_name.a.get("href")
            detailUrl = url + "zhuanjia.html"
            detail_soup = BeautifulSoup(requests.get(detailUrl).text, "lxml")
            hpdoc_table_div = detail_soup.find_all("table", class_="hpdoc_table")
            for hpdoc_table_info in hpdoc_table_div:
                office_class = hpdoc_table_info.find_all("td", class_="tdl")



