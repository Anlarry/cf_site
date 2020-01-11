from __future__ import absolute_import,unicode_literals
from celery import shared_task
import time
from cf_robot.get_problem import Get_problem, get_all_pagenum
from cf_robot.get_pro_detail import Get_pro_detail
from cf_robot.log_submit import Log_Submit 
from cf_robot.Updata_status import get_status_by_id
from .models import problem, problem_detail, user_problem_status
import pandas as pd

@shared_task
def add(x, y):
    time.sleep(2)
    print(x+y) 
    # return x + y

@shared_task
def update_problem():
    print('updata_start...')
    all_pages = get_all_pagenum()
    T = Get_problem(1, all_pages+1)
    ids, names, tags, dif = [], [], [], []
    my_ids = []
    urls = []
    now_id = 1
    for each in T.problem:
        # print('Update',each['pro_id'], each['url'])
        my_ids.append(each['my_id'])
        ids.append(each['pro_id'])
        names.append(each['name'])
        tags.append(','.join(each['tags']))
        dif.append(each['dif']) 
        urls.append(each['url'])
        try:
            the_pro = problem.objects.get(pro_id=each['pro_id'])
            now_pro_id = each['pro_id']
            now_my_id = each['my_id']
            now_name = each['name']
            now_tags = each['tags']
            now_dif = each['dif']
            now_url = each['url']
            if now_dif == '':
                now_dif = -1
            else:
                now_dif = int(now_dif)
            if  the_pro.url != now_url or the_pro.my_id != now_my_id or now_pro_id != the_pro.pro_id or now_name != the_pro.name or ','.join(now_tags) != the_pro.tags or now_dif != the_pro.dif:
                the_pro.url = now_url
                the_pro.pro_id = now_pro_id##
                the_pro.my_id = now_my_id
                the_pro.name = now_name
                the_pro.tags = now_tags
                the_pro.dif = now_dif
                the_pro.save()
                print('Updata New', now_pro_id, now_url)
        except problem.DoesNotExist:
            if each['dif'] == '':
                each['dif'] = -1
            now_pro = problem(url=each['url'], my_id=each['my_id'],pro_id=each['pro_id'], name=each['name'], tags=each['tags'], dif=each['dif'])    
            now_pro.save()
            print('Save New', each['pro_id'], each['url'])
        now_id += 1
    data = pd.DataFrame({'my_id':my_ids,'pro_id':ids, 'name':names, 'tags':tags, 'dif':dif, 'url':urls})
    # data.to_csv('cf_robot/all_problem.csv')
    # for i in range(1, all_pages+1):
    #     now_page_pro = Get_problem.get_page_pro(i)
    #     print('----Update Page %d----'%i)
    #     for each in now_page_pro:
    #         print('Update',each['pro_id'])
    #         ids.append(each['pro_id'])
    #         names.append(each['name'])
    #         tags.append(','.join(each['tags']))
    #         dif.append(each['dif'])
    #         
@shared_task
def update_problem_detail(url, has_detail=False):
    # print('update problem')
    T = Get_pro_detail(url='http://codeforces.com/'+url)
    if has_detail:
        pass
        # the_pro_detail = problem_detail.objects.get(url=url)
        # if (the_pro_detail.text != T.text or the_pro_detail.in_file != T.in_file or
        #     the_pro_detail.out_file != T.out_file or the_pro_detail.time_lim != T.time_lim
        #     or the_pro_detail.mem_lim != T.mem_lim):
        #     the_pro_detail.mem_lim = T.mem_lim
        #     the_pro_detail.time_lim = T.time_lim
        #     the_pro_detail.in_file = T.in_file
        #     the_pro_detail.out_file = T.out_file
        #     the_pro_detail.text = T.text
        #     the_pro_detail.save()
        #     print('New problem detail %s'%url)
    else:
        now_pro_detail = problem_detail(url=url, time_lim=T.time_lim,mem_lim=T.mem_lim,in_file=T.in_file,out_file=T.out_file, text=T.text) 
        now_pro_detail.save()
        print('New problem detail %s'%url)
        return now_pro_detail

@shared_task
def submit(name, password, pro_id, scr):
    print(name+' try '+pro_id)
    T = Log_Submit(name,password)
    ok = T.login()
    if scr == "" or scr == None:
        print('scr is ""')
        return
    ok = ok and T.submit(pro_id, scr, lan=54)
    if ok :
        time.sleep(2)
        res, tim, mem = T.get_submit_result()
        now_id = T.submit_id
        ac = 'Accept' in res or 'Happy New Year' in res
    else :
        res = 'submit Fail'
        tim, mem = "", ""
        now_id = "0"
        ac = False
    try :
        last_sub = user_problem_status.objects.get(name=name,pro_id=pro_id)
        last_sub.last_sta = res
        last_sub.is_ac = last_sub.is_ac or ac
        last_sub.last_id = now_id
        last_sub.time = tim
        last_sub.memory = mem
        last_sub.save()
        print('try again', res)
    except user_problem_status.DoesNotExist:
        now_sub = user_problem_status(name=name, pro_id=pro_id,last_sta=res, is_ac = ac, last_id=now_id, time=tim,memory=mem)
        now_sub.save()
        print('first submit', res)

@shared_task
def update_submit_status(name, password,pro_id, contest_id, last_sub_id):
    # T = Log_Submit(name, password)
    if last_sub_id == 0:
        print('last submit is "Fail"')
        return
    print('updata submit status')
    last_sub_sta = user_problem_status.objects.get(name=name, pro_id=pro_id) 
    last_sub_sta.last_sta,last_sub_sta.time,last_sub_sta.memory = get_status_by_id(str(contest_id), str(last_sub_id))
    last_sub_sta.is_ac = last_sub_sta.is_ac or ('Accept' in last_sub_sta.last_sta) or ('Happy New Year' in last_sub_sta.last_sta)
    print(last_sub_sta.last_sta, last_sub_sta.time, last_sub_sta.memory)
    last_sub_sta.save()
# ids, names, tags, dif = [], [], [], []
# for each in T.problem:
#     ids.append(each['pro_id'])
#     names.append(each['name'])
#     tags.append(','.join(each['tags']))
#     dif.append(each['dif'])
# data = pd.DataFrame({'pro_id':ids, 'name':names, 'tags':tags, 'dif':dif})
# data.to_csv('all_problem.csv')
# update_problem()