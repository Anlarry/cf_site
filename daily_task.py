import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'cf_site.settings')
import django
django.setup()

from cf_robot.get_problem import Get_problem, get_all_pagenum
from cf_robot.get_pro_detail import Get_pro_detail
from cf_robot.log_submit import Log_Submit 
from cf_robot.Updata_status import get_status_by_id
from cf.models import problem, problem_detail, user_problem_status
from cf.task import update_problem

update_problem()
