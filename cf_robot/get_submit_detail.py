import requests
from bs4 import BeautifulSoup
from cf_robot.log_submit import user_agent
import  random
def get_submit_detail(contest_id,submit_id):
    contest_id = str(contest_id)
    submit_id = str(submit_id)
    s = requests.session()
    agent = random.choice(user_agent)
    header={'User-Agent' : agent}
    s.headers.update(header)
    url = "http://codeforces.com/problemset/submission/"+contest_id+'/' + submit_id
    html = s.get(url).text
    bs = BeautifulSoup(html, "lxml")
    X_Csrf_Token = bs.find(attrs={'name':'X-Csrf-Token'}).attrs['content']
    url = 'http://codeforces.com/data/submitSource'
    data = {
        'submissionId':submit_id,
        'csrf_token':X_Csrf_Token,
    }
    res = s.post(url, data=data)
    res = eval(res.text)
    source = res['source']
    in_out_data = []
    tests_count = int(res['testCount'])
    for i in range(1, 1+tests_count):
        in_out_data.append({"input":res['input#'+str(i)], "output":res['output#'+str(i)], "answer":res['answer#'+str(i)], 'status':res['checkerStdoutAndStderr#'+str(i)]})
    # print(source, '\n', in_out_data)
    return {"source":source, "test_data":in_out_data}

# res = get_submit_detail('66184913')
# print(res['source'])
# for each in res['test_data']:
#     print(each['input'], each['answer'])