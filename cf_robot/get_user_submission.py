from bs4 import BeautifulSoup
import  requests
from .log_submit import  Log_Submit

class GetUserSubmission(Log_Submit):
    def __init__(self, name, password):
        Log_Submit.__init__(self, name, password)
        self.submission_html = self.get_submission()
    
    def get_submission(self):
        if not self.login():
            return None
        url = "http://codeforces.com/submissions/"+self.name
        html = self.s.get(url).text
        bs = BeautifulSoup(html, 'lxml')
        tag = bs.find('table', attrs={'class':'status-frame-datatable'})
        sub_tags = tag.find_all('a')
        i = 0
        while i < len(sub_tags):
            contest_url = sub_tags[i+2].attrs['href']
            info = contest_url.split('/')
            sub_tags[i].attrs['href'] = '/cf/submit/'+info[-3]+'/'+sub_tags[i].attrs['submissionid']
            sub_tags[i+1].attrs['href'] = '/cf/'+sub_tags[i+1].get_text()
            sub_tags[i+2].attrs['href'] = '/cf/problem/'+info[-3]+info[-1]
            i += 3
        return str(tag)
