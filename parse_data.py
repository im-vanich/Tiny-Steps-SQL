import json
import data

with open('data/goals.json', 'w', encoding='utf-8') as f:
    json.dump(data.goals, f, ensure_ascii=False)

with open('data/teachers.json', 'w', encoding='utf-8') as f:
    json.dump(data.teachers, f, ensure_ascii=False)


