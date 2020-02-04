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
from django.template.loader import get_template
import markdown

def user_view(request, name):
    # submissions = user_problem_status.objects.get(name=name)
    submissions = [x for x in user_problem_status.objects.all() if x.name == name]
    solved = [x.pro_id for x in filter(lambda x: x.is_ac, submissions)]
    unsolved = [x.pro_id for x in filter(lambda x: not x.is_ac,submissions)]
    solved = sorted(solved, key=lambda x: problem.objects.get(pro_id=x).my_id, reverse=True)
    unsolved = sorted(unsolved, key=lambda x: problem.objects.get(pro_id=x).my_id, reverse=True)
    solved = [solved[i:i+10] for i in range(0, len(solved), 10)]
    unsolved = [unsolved[i:10] for i in range(0, len(unsolved), 10)]
    return render(request, 'cf/user_view.html',{
        'name':name,
        'submissions':submissions,
        'solved':solved,
        'unsolved':unsolved,
    })
