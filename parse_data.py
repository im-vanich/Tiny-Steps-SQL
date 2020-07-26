import json
from app import Teacher, Student, Request, Goal, Booking, db


# import data
#
# with open('data/goals.json', 'w', encoding='utf-8') as f:
#     json.dump(data.goals, f, indent=4, ensure_ascii=False)
#
# with open('data/teachers.json', 'w', encoding='utf-8') as f:
#     json.dump(data.teachers, f, indent=4, ensure_ascii=False)


def load_db():
    with open('data/teachers.json', 'r', encoding='utf-8') as r:
        get_info = json.load(r)

    for info in get_info:
        teacher = Teacher(name=info['name'], about=info['about'], rating=info['rating'], picture=info['picture'],
                          price=info['price'])
        db.session.add(teacher)

    with open('data/goals.json', 'r', encoding='utf-8') as r:
        goals = json.load(r)

    for goal in goals:
        goal_to_study = Goal(goal_to_study=goal)
        db.session.add(goal_to_study)

    db.session.commit()


if __name__ == '__main__':
    load_db()
