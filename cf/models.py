from django.db import models

class TagFeild(models.CharField):
    def __init__(self, *args, **kargs):
        super(TagFeild, self).__init__(*args, **kargs)
    def to_python(self, value):
        if value == "":
            value = []
        else:
            value = value.split(',')
        return value
    def get_prep_value(self, value):
        return ','.join(value)
    def value_to_string(self, value):
        return ','.join(value)
# Create your models here.
class problem(models.Model):
    my_id = models.IntegerField(default=0)
    pro_id = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    tags = TagFeild(max_length=200)
    dif = models.IntegerField(default=0)
    url = models.CharField(max_length=200,default="")
    def __str__(self):
        return self.pro_id+' '+self.name

# class DataField(models.TextField):
#     def __init__(self, *args, **kargs):
#         super(DataField, self).__init__(*args, **kargs)
#     def to_python(self, value:str):
#         res = []
#         for each in value.split('@@'):
#             each = each.split('@')
#             res.append({'input':each[0], 'output':each[1]})
#         return res 
#     def get_prep_value(self, value):
#         res = [each['input']+'@'+each['output']  for each in value]
#         return '@@'.join(res)
#     def  __str__(self, value):
#         res = [each['input']+'@'+each['output']  for each in value]
#         return '@@'.join(res)

class problem_detail(models.Model):
    url = models.CharField(max_length=200)
    time_lim = models.CharField(max_length=200)
    mem_lim = models.CharField(max_length=200)
    in_file = models.CharField(max_length=200)
    out_file = models.CharField(max_length=20)
    text = models.TextField() # html str

class user_problem_status(models.Model):
    pro_id = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    last_sta = models.CharField(max_length=200)
    is_ac = models.BooleanField(default=False)
    time = models.CharField(max_length=200)
    memory = models.CharField(max_length=200)
    last_id = models.IntegerField(default=0)

class news(models.Model):
    title = models.CharField(max_length = 200,default = "")
    text = models.TextField()
    top = models.BooleanField(default=False)
    def __str__(self):
        return self.title
     

