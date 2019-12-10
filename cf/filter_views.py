from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import problem, user_problem_status, news
from .load_problem import load_problem
from .task import update_problem,add,submit,update_submit_status
from .user import Create_new_user,Check_user
from django.contrib.auth.models import User
from .model_funs import get_ordered_pro,get_pro_detail,get_pro_by_tags
from django.contrib.auth import login, authenticate,logout
from cf_robot.get_submit_detail import get_submit_detail
from django.template.loader import get_template
import markdown

def dif_filter(request, from_dif, to_dif,page_id):
    try:
        url = '/cf/problem/dif-'+from_dif+'-'+to_dif
        from_dif, to_dif = map(lambda x: 1e5 if x == 'inf' else x, (from_dif, to_dif))
        from_dif = int(from_dif)
        to_dif = int(to_dif)    
        all_pro = filter(lambda x: from_dif <= x.dif <= to_dif,problem.objects.all())
        all_pro = sorted(all_pro, key=lambda x: x.my_id,reverse=True)
        all_page = (len(all_pro) + 99) // 100
        pros = all_pro[100*page_id-100:min(100*page_id, len(all_pro))]
        return render(request, 'cf/filter.html', {
            'title':'CF problem here','pros':pros, 'page_id':page_id, 'all_page':all_page,
            'range_1_to_now_page':range(1,page_id+1),
            'range_now_page_to_all':range(page_id+1, all_page+1),
            'filter_url':url
        }) 
    except ValueError:
        all_pro = len(problem.objects.all())
        all_page = (len(problem.objects.all()) + 99)// 100
        pros = get_ordered_pro()[100*1-100:min(100*1, all_pro)]
        return render(request, 'cf/title.html', {
            'title':'CF problem here','pros':pros, 'page_id':1, 'all_page':all_page,
            'range_1_to_now_page':range(1,1+1),
            'range_now_page_to_all':range(1+1, all_page+1)
        }) 

def tag_filter(request, tags, page_id):
    url = '/cf/problem/tag-'+tags 
    # tags = tags.split(',')
    all_pro = get_pro_by_tags(tags)
    all_page = (len(all_pro)+99) // 100
    pros = all_pro[100*page_id-100:min(100*page_id, len(all_pro))]
    return render(request, 'cf/filter.html', {
            'title':'CF problem here','pros':pros, 'page_id':page_id, 'all_page':all_page,
            'range_1_to_now_page':range(1,page_id+1),
            'range_now_page_to_all':range(page_id+1, all_page+1),
            'filter_url':url,
        }) 

