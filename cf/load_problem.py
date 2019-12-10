import cf_robot
import pandas as pd
from .models import problem
def load_problem():
    pros = pd.read_csv('cf_robot/all_problem.csv')
    for idx, row in pros.iterrows():
        try:
            tags = row['tags'].split(',')
        except :
            tags = []
        try:
            dif = int(row['dif'])
        except :
            dif = -1
        print(tags)
        pro = problem(my_id=row['my_id'],pro_id=row['pro_id'], name=row['name'], tags=tags, dif=dif, url=row['url']) 
        pro.save()
    return 