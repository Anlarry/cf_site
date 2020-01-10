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
# from cf_robot.log_submit import Log_Submit 
# Create your views here.

def home(request):
    try:
        print(request.session['name'])
        name = request.session['name']
    except KeyError:
        name = ""
    # the_news = sorted(list(news.objects.all()), lambda x: x.id, reversed=True)[:5]
    the_news = news.objects.order_by('-id')[:5]
    return render(request, 'cf/home.html',{
        'name': name,
        'news':the_news,
    })

def log_in(request, name=""):
    if request.method == 'POST':
        name = request.POST.get('name')
        pwd = request.POST.get('password')
        user = authenticate(request,username=name,password=pwd)
        if user is not None:
            login(request,user)
            request.session['name'] = name
            request.session['password'] = pwd
            return redirect("/cf") 
        else:
            return render(request, 'cf/log_in.html',{
                "name":'Wrong Password!'
            })
    else:
        return render(request, 'cf/log_in.html',{
            "name":name,
        })

def ulog_in(request, name):
    return render(request, 'cf/log_in.html',{
        "name":name,
    })

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        pwd = request.POST.get('password')
        email = request.POST.get('email')
        # print(name, pwd, email)
        res = Create_new_user(name, pwd, email)
        if res:
            return redirect('/cf/log_in/'+name)
        else:
            return render(request, 'cf/register.html',{
                "msg":'User Exist'
            })
    else:
        return render(request, 'cf/register.html',{
            "msg":"",
        })

def title(request):
    if len(problem.objects.all()) == 0:
        load_problem()
    updata_res = update_problem()
    # update_problem()
    # pros = problem.objects.all()[:100]
    pros = get_ordered_pro()[:100]
    all_page = (len(problem.objects.all()) + 99)// 100
    print('*****', all_page)
    res = add(4, 4)
    # print(res.ready()) 
    return render(request, 'cf/title.html', {
        'title':'CF problem here','pros':pros, 'page_id':1, 'all_page':all_page,
        'range_1_to_now_page':range(1,1+1),
        'range_now_page_to_all':range(1, all_page)
       })
    # return HttpResponse('All CF problem here')

def page(request, page_id):
    all_pro = len(problem.objects.all())
    all_page = (len(problem.objects.all()) + 99)// 100
    pros = get_ordered_pro()[100*page_id-100:min(100*page_id, all_pro)]
    return render(request, 'cf/title.html', {
        'title':'CF problem here','pros':pros, 'page_id':page_id, 'all_page':all_page,
        'range_1_to_now_page':range(1,page_id+1),
        'range_now_page_to_all':range(page_id+1, all_page+1)
       }) 

def problem_page(request, pro_id):
    pro = problem.objects.get(pro_id=pro_id)
    contest_id = pro.url.split('/')[-2]
    pro_detail = get_pro_detail(url=pro.url)
    try:
        name = request.session['name']
    except KeyError:
        name = ""
    # print(pro_detail.text)
    if name != "":
        try:
            last_sta = user_problem_status.objects.get(name=name,pro_id=pro_id)
            update_submit_status(name, request.session['password'],pro_id, contest_id, last_sta.last_id)        
            sta = last_sta.last_sta
            tim = last_sta.time
            mem = last_sta.memory
            is_ac = last_sta.is_ac
            last_submit_id = last_sta.last_id
        except user_problem_status.DoesNotExist:
            sta = ""
            tim, mem = "", ""
            is_ac = False
    else:
        sta = ""
        tim = ""
        mem = ""
        is_ac = False
    if sta == "":
        last_submit_id = 0
    if request.method == 'POST':
        if name != "":
            src = request.POST.get('code')
            # user = User.objects.get(username=name)
            password = request.session['password']
            submit(name, password, pro_id, src)
            # request.method='GET'
            return redirect('/cf/problem/'+pro_id)
            # return render(request, 'cf/problem_page.html',{
            #     'name':pro.name,
            #     'url':pro.url,
            #     'pro_id':pro_id,
            #     'text':pro_detail.text.replace('/predownloaded', 'http://codeforces.com//predownloaded'),
            #     'time_lim':pro_detail.time_lim,
            #     'mem_lim':pro_detail.mem_lim,
            #     'in_file':pro_detail.in_file,
            #     'out_file':pro_detail.out_file,
            #     'status':sta,
            #     }) 
        else:
            return redirect('/cf/log_in/')
    else:
        return render(request, 'cf/problem_page.html',{
            'name':pro.name,
            'url':pro.url,
            'pro_id':pro_id,
            'text':pro_detail.text.replace('/predownloaded', 'http://codeforces.com//predownloaded'),
            'time_lim':pro_detail.time_lim,
            'mem_lim':pro_detail.mem_lim,
            'in_file':pro_detail.in_file,
            'out_file':pro_detail.out_file,
            'status':sta,
            'time':tim,
            'memory':mem,
            "is_ac":is_ac,
            'last_submit_id':last_submit_id,
            'contest_id':int(contest_id),
        })
  
def log_out(request):
    logout(request)
    # print(request.session['name'])
    return redirect('/cf')

def submit_detail(request, contest_id, submit_id):
    res = get_submit_detail(contest_id,submit_id)
    src = res['source']
    test_data = res['test_data']
    print('test_data geted')
    input = [each['input'] for each in test_data]
    output = [each['output'] for each in test_data]
    answer = [each['answer'] for each in test_data]
    status = [each['status'] for each in test_data]
    return render(request, 'cf/submit_detail.html',{
        "src":src,
        'test_data':zip(input, output,answer, status),
    })

def news_page(request, news_id):
    new = news.objects.get(id=news_id)
    context = new.text
    config = {
            'codehilite': {
            'use_pygments': False,
            'css_class': 'prettyprint',
        }
    }
    html = markdown.markdown(context, extensions=[
        'markdown.extensions.extra',
        'codehilite',
        'markdown.extensions.toc',
    ],extension_configs=config)
    return render(request, 'cf/news.html',{
        'html':html,
        'title':new.title,
    })