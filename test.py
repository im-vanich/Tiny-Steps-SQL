import json
import random

with open('data/teachers.json', 'r') as f:
    teachers_list = json.load(f)

# te = []
# for i in range(6):
#     te.append(random.choice(teachers_list))
# print(te)

a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
b = []

print(random.sample(a,6))
