import requests
from bs4 import BeautifulSoup
import re, random
# from  cf_robot.log_submit import user_agent
def get_tutorial(pro_id, problem_url):
    html = requests.get(problem_url).text
    bs = BeautifulSoup(html, 'lxml')
    try:
        tag = bs.find('div', attrs={'class':'roundbox sidebox sidebar-menu'})
        tag = bs.find('a', text=re.compile(r'Tutorial.*'))
        # tutorial_url =  "http://codeforces.com" + tag.attrs['href']
        if 'codeforces' in tag.attrs['href']:
            tutorial_url = tag.attrs['href']
        else:
            tutorial_url = "http://codeforces.com" + tag.attrs['href']
        return get_tutorial_from_blog(pro_id, tutorial_url)
    except AttributeError:
        return None
    # with open('tmp.html', 'w') as F:
    #     print(html, file=F)
    # pass

def get_tutorial_from_blog(pro_id, tutorial_url):
    s = requests.session()
    # agent = random.choice(user_agent)
    # header={'User-Agent' : agent}
    # s.headers.update(header)
    html = s.get(tutorial_url).text
    with open('tmp.html', 'w') as F:
        print(html, file=F)
    bs = BeautifulSoup(html, 'lxml')
    X_Csrf_Token = bs.find(attrs={'name':'X-Csrf-Token'}).attrs['content']
    data = {
        'problemCode':pro_id,
        'csrf_token':X_Csrf_Token,
    }
    url = "http://codeforces.com/data/problemTutorial"
    res = s.post(url, data=data).text
    res = eval(res)
    tutorial_html = res['html']
    try:
        tags = bs.find('div', attrs={'class':'ttypography'}).find_all('div', attrs={'class':'spoiler-content', 'style':'display: none;'})
        res = [x.get_text() for x in tags if x.get_text() != 'Tutorial is loading...']
        code = res[ord(pro_id[-1])-ord('A')]
    except  :
        code = None 
    return tutorial_html, code

# get_tutorial('1302H','https://codeforces.com/problemset/problem/1302/H')