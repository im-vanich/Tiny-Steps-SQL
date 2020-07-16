import json
from app import

with open('data/teachers.json', 'r') as f:
    teachers_list = json.load(f)

day_info = teachers_list[0]['free']
teachers_info = teachers_list[0]
print(day_info)

a =

