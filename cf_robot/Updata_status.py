import requests
from bs4 import BeautifulSoup
import re

def get_status_by_id(contest_id, sub_id):
    url = "https://codeforces.com/problemset/submission/"+contest_id+'/'+sub_id
    print(url)
    html = requests.get(url).text
    # with open('cf_robot/tmp.html', 'w') as F:
    #     print(html, file=F)
    bs = BeautifulSoup(html, "lxml")
    tag = bs.find(lambda x: x.get_text()==sub_id)
    new_sta = tag.parent.find_all('td')[4].get_text()
    new_sta = new_sta.strip()
    return new_sta
# get_status_by_id('1257', '66111825')
# 1257 
# 66111825