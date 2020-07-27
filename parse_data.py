import json
from app import Teacher, Student, Request, Goal, Booking, db, TeacherFeatures


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

    for teacher in get_info:
        teacher_list = teacher['goals']
        for goal in teacher_list:
            query_goal_id = db.session.query(Goal.id).filter(Goal.goal_to_study == goal).first()[0]
            teacher_id = int(teacher['id'] + 1)
            teacher_features = TeacherFeatures(teacher_id=teacher_id, goal_id=query_goal_id)
            db.session.add(teacher_features)

    db.session.commit()


if __name__ == '__main__':
    load_db()
