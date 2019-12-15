import requests
from bs4 import BeautifulSoup
import random
import re
import time
import threading

user_agent = [
	'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 '
	'Safari/534.50',
	'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
	'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',
	'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; '
	'.NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko',
	'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
	'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
	'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
	'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
	'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
	'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
	'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 '
	'Safari/535.11',
	'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
	'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
	'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
	'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
	'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR '
	'2.0.50727; SE 2.X MetaSr 1.0)',
	'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
	'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)',
	'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
	'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) '
	'Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
	'Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) '
	'Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
	'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 '
	'Mobile/8J2 Safari/6533.18.5',
	'Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) '
	'Version/4.0 Mobile Safari/533.1',
	'MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 ('
	'KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
	'Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10',
	'Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 '
	'Safari/534.13',
	'Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile '
	'Safari/534.1+',
	'Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 '
	'Safari/534.6 TouchPad/1.0',
	'Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) '
	'AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124',
	'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)',
	'UCWEB7.0.2.37/28/999',
	'NOKIA5700/ UCWEB7.0.2.37/28/999',
	'Openwave/ UCWEB7.0.2.37/28/999',
	'Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999', ]

class Log_Submit:
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.s = requests.session()
        self.submit_id = ""

    def login(self):
        agent = random.choice(user_agent)
        header={'User-Agent' : agent}
        self.s.headers.update(header)
        try:
            res = self.s.get('http://codeforces.com/enter?back=%2F')
            soup=BeautifulSoup(res.text,'lxml')
            csrf_token=soup.find(attrs={'name' : 'X-Csrf-Token'}).get('content')
            form_data={
                'csrf_token' : csrf_token,
                'action' : 'enter',
                'ftaa' : '',
                'bfaa' : '',
                'handleOrEmail' : self.name,
                'password' : self.password,
                'remember' : []
            }
            rps = self.s.post('http://codeforces.com/enter',data=form_data)
            print(rps)
            bs = BeautifulSoup(rps.text, 'lxml')
            if bs.find(attrs={'class':'error for__password'}) != None:
                print('wrang user info')
                return False
            else:
                return True 
            # with open('cf_robot/tmp.html', 'w') as F:
            #     print(rps.text, file=F)
        except Exception as e:
            print('Log in failed -> ',e)
            return False
    def submit(self, pro_id, code, lan):
        res= self.s.get('http://codeforces.com/problemset/submit')
        soup=BeautifulSoup(res.text,'lxml')
        csrf_token=soup.find(attrs={'name' : 'X-Csrf-Token'}).get('content')
        post_data={
            'csrf_token' : csrf_token,
            'ftaa' : '',
            'bfaa' : '',
            'action' : 'submitSolutionFormSubmitted',
            'submittedProblemCode' : pro_id,
            'programTypeId' : str(lan),
            'source' : code,
            'tabSize' : 4,
            'sourceFile' : '',
        }
        res= self.s.post('http://codeforces.com/problemset/submit?csrf_token='+csrf_token,data=post_data)
        if res.status_code!=200 :
            print(pro_id,'Submit fail...')
            print(res)
            return False
            exit(0)
        else:
            print(pro_id,'Submit successfully!')
            return True
    def get_submit_result(self):
        url = "https://codeforces.com/submissions/" + self.name
        res = self.s.get(url)
        print(res)
        html = res.text
        # with open('cf_robot/tmp.html', 'w') as F:
        #     print(html, file=F)
        bs = BeautifulSoup(html, "lxml")
        self.submit_id = bs.find(attrs={'class':'hiddenSource'}).get_text()
        verdict = bs.find(attrs={'submissionid':self.submit_id}).get_text()
        print(verdict)
        return verdict
    def get_status(self):
        url = "https://codeforces.com/data/submitSource"
        agent = random.choice(user_agent)
        html = self.s.get('https://codeforces.com/submissions/'+self.name).text
        bs = BeautifulSoup(html, 'lxml')
        X_Csrf_Token = bs.find(attrs={'name':'X-Csrf-Token'}).attrs['content']
        headers ={
            "Referer":'https://codeforces.com/submissions/__Wind__',
            "X-Csrf-Token": X_Csrf_Token,
            "X-Requested-With":"XMLHttpRequest",
            'User-Agent' : agent,
        }
        data = {
            'submissionId':self.submit_id,
            'csrf_token':X_Csrf_Token,
        }
        res = self.s.post(url, data=data)
        # print(res)
        res = eval(res.text)
        source = res['source']
        in_out_data = []
        tests_count = int(res['testCount'])
        for i in range(1, 1+tests_count):
            in_out_data.append({"input":res['input#'+str(i)], "output":res['output#'+str(i)], "answer":res['answer#'+str(i)]})
        # print(source, '\n', in_out_data)
        return {"source":source, "test_data":in_out_data}
        # with open('cf_robot/tmp.html', 'w') as F:
        #     print(res.text, file=F)
    def get_status_by_id(self,contest_id, sub_id):
        # html = self.s.get('')
        # X_Csrf_Token = bs.find(attrs={'name':'X-Csrf-Token'}).attrs['content']
        url = "https://codeforces.com/problemset/submission/"+contest_id+'/'+sub_id
        html = self.s.get(url).text
        # with open('cf_robot/tmp.html', 'w') as F:
        #     print(html, file=F)
        bs = BeautifulSoup(html, "lxml")
        tag = bs.find(lambda x: x.get_text()==sub_id)
        new_sta = tag.parent.find_all('td')[4].get_text()
        new_sta = new_sta.strip()
        return new_sta
# user = ''
# password = ''
# code = '''
#     include<iosteam>
#     using namespace std;
#     int main(){
#         cout << "1" <<"\n";
#     }
# '''
# T = Log_Submit(user, password)
# T.login()
# T.submit('1000A',  code, lan=54)
# T.get_submit_result()
# T.submit_id = '65237395'
# T.get_status()
# T = Log_Submit('__Wind__', '654183')
# T.get_status_by_id('1257', '66111825')