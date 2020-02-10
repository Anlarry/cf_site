from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import problem, user_problem_status, news
from .load_problem import load_problem
from .task import update_problem,add,submit,update_submit_status
from .user import Create_new_user,Check_user
from django.contrib.auth.models import User
from .model_funs import get_ordered_pro,get_pro_detail
from django.contrib.auth import login, authenticate,logout
from cf_robot.get_submit_detail import get_submit_detail
from cf_robot.get_tutorial import get_tutorial
from django.template.loader import get_template
import markdown

from bs4 import BeautifulSoup

def tutorial_view(request, pro_id):
    problem_url = "https://codeforces.com" + problem.objects.get(pro_id=pro_id).url
    tutorial_html, code = get_tutorial(pro_id, problem_url)
    bs = BeautifulSoup(tutorial_html, 'lxml')
    bs.find('a').attrs['href'] = '/cf/problem/'+pro_id
    return render(request, 'cf/tutorial.html',{
        'tutorial_html': str(bs),
        'code':code,
    })