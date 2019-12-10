import requests
from bs4 import BeautifulSoup
import pandas as pd

class Get_problem:
    "get problem from start page to end page"
    url = 'http://codeforces.com/problemset/page/' # + num
    def __init__(self, sp, ep):
        self.problem = []
        for i in range(sp, ep):
            self.problem += Get_problem.get_page_pro(i)
            print('%d page done \r'%(i), end='')
        now_id = 1
        for i in range(len(self.problem)-1, -1, -1):
            self.problem[i]['my_id'] = now_id
            now_id += 1
    @staticmethod
    def get_page_pro(page)->list: 
        page_url = Get_problem.url + str(page)
        html = requests.get(page_url).text.replace('\r\n','')
        bs = BeautifulSoup(html, 'lxml')
        pros = bs.find_all('tr')
        res = []
        for i in range(1, len(pros)-1):
            res.append(Get_problem.get_one_pro(pros[i]))
        return res
    @staticmethod
    def get_one_pro(tag)->dict:
        info = ['pro_id', 'name', 'tags', 'dif']
        # tag = tag.replace('\r\n', '')
        tds = tag.find_all('td')
        pro_id = tds[0].a.get_text()
        pro_url = tds[0].a.attrs['href']
        name = tds[1].div.a.get_text()
        # tags = tds[1].div.next_sibling.find_all('a')
        tags = tds[1].find_all('div')[1].find_all('a')
        try:
            tags = [s.get_text().strip() for s in tags]
        except AttributeError:
            tags = ['']
        try:
            dif = tds[3].span.get_text()
        except AttributeError:
            dif = ''
        return {'my_id':0, 'pro_id':pro_id.strip(), 'name':name.strip(), 'tags':tags, 'dif':dif.strip(), 'url':pro_url}

def get_all_pagenum():
    url = 'http://codeforces.com/problemset'
    html = requests.get(url).text
    bs = BeautifulSoup(html, 'lxml')
    page_index = bs.find_all('span', attrs={'class':'page-index'})
    last_page = page_index[-1].attrs['pageindex']
    return int(last_page)

# print(get_all_pagenum())
# T = Get_problem(1, 57)
# ids, names, tags, dif = [], [], [], []
# for each in T.problem:
#     ids.append(each['pro_id'])
#     names.append(each['name'])
#     tags.append(','.join(each['tags']))
#     dif.append(each['dif'])
# data = pd.DataFrame({'pro_id':ids, 'name':names, 'tags':tags, 'dif':dif})
# data.to_csv('all_problem.csv')
# with open('out', 'w') as F:
#     for each in T.problem:
#         print(each, file=F)