from django.db import models
from .models import problem, problem_detail
from .task import update_problem_detail

# def cmp_key(pro1:problem):
#     num1 = 0
#     id1 = ""
#     i = 0
#     while i < len(pro1.pro_id):
#         c = pro1.pro_id[i]
#         if '0' <= c <= '9':
#             num1 = num1 * 10 + ord(c) - ord('0')
#         else:
#             break
#         i += 1
#     id1 = pro1.pro_id[i:]
#     return (num1, id1)

def get_ordered_pro():
    all_pro = problem.objects.all()
    all_pro = sorted(all_pro, key=lambda pro: pro.my_id, reverse=True)
    return all_pro

def get_pro_detail(url):
    try:
        pro_detail = problem_detail.objects.get(url=url)
        # update_problem_detail(url=pro_detail.url,has_detail=True)
    except problem_detail.DoesNotExist:
        pro_detail = update_problem_detail(url=url)
    return pro_detail

def get_pro_by_tags(tags):
    tags = tags_set(tags)
    res = [pro for pro in problem.objects.all() if tags.issubset(tags_set(pro.tags))]
    return sorted(res, key=lambda x: x.my_id,reverse=True)

def tags_set(tags):
    return {x for x in tags.split(',')}