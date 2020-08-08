import requests
from bs4 import BeautifulSoup

class Get_pro_detail:
    def __init__(self, url):
        html = requests.get(url).text.replace('<br>', '\n')
        bs = BeautifulSoup(html, 'lxml')
        tag = bs.find('div', attrs={'class': 'time-limit'})
        self.time_lim = tag.contents[-2].get_text() + ': ' + tag.contents[-1]
        tag = bs.find('div', attrs={'class': 'memory-limit'})
        self.mem_lim = tag.contents[-2].get_text() + ': ' + tag.contents[-1]
        tag = bs.find('div', attrs={'class': 'input-file'})
        self.in_file = tag.contents[-2].get_text() + ': ' + tag.contents[-1]
        tag = bs.find('div', attrs={"class": 'output-file'})
        self.out_file = tag.contents[-2].get_text() + ': ' + tag.contents[-1]
        all_tag = bs.find('div', attrs={'class': 'problem-statement'})
        self.text = ""
        for each in all_tag.div.next_siblings:
            self.text += str(each)



# T = Get_pro_detail('http://codeforces.com//problemset/problem/1261/F')

