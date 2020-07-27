import random
import json
import os
import app_form
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = 'very-Secret-Key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tiny.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Models for database

teachers_goal = db.Table('teachers_goal',
                         db.Column('teacher_id', db.Integer, db.ForeignKey('teachers.id')),
                         db.Column('goals_id', db.Integer, db.ForeignKey('goals.id')))


class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    about = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    picture = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    booking = db.relationship('Booking')
    goals = db.relationship('Goal', secondary=teachers_goal)


class Booking(db.Model):
    __tablename__ = 'booking'

    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    teacher = db.relationship('Teacher')
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    student = db.relationship('Student', back_populates='booking')
    study_day = db.Column(db.String, nullable=False)
    study_time = db.Column(db.String, nullable=False)


class Request(db.Model):
    __tablename__ = 'requests'

    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.String, nullable=False)
    free_time = db.Column(db.String, nullable=False)
    student_name = db.Column(db.String, nullable=False)
    student_phone = db.Column(db.String, nullable=False)


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String, nullable=False, unique=True)
    student_phone = db.Column(db.String, nullable=False, unique=True)
    booking = db.relationship('Booking', back_populates='student')


class Goal(db.Model):
    __tablename__ = 'goals'

    id = db.Column(db.Integer, primary_key=True)
    goal_to_study = db.Column(db.String, nullable=False)
    teachers = db.relationship('Teacher', secondary=teachers_goal)


class TeacherFeatures(db.Model):
    __tablename__ = 'teacher_features'

    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"))
    teacher = db.relationship("Teacher")
    goal_id = db.Column(db.Integer, db.ForeignKey("goals.id"))
    goal = db.relationship("Goal")


@app.route('/')
def render_index():
    teacher = db.session.query(Teacher).order_by(Teacher.id).all()
    teacher_random = random.sample(teacher, 6)
    goals_query = db.session.query(Goal.goal_to_study).all()
    goals_list = []
    for goal in goals_query:
        goals_list.append(goal[0])
    return render_template('index.html', teachers=teacher_random, goals=goals_list)


@app.route('/goals/<goal>/')
def render_goals(goal):
    goals_query = db.session.query(Goal.goal_to_study).all()
    goals_list = []
    for main_goal in goals_query:
        goals_list.append(main_goal[0])
    query_gol_id = db.session.query(Goal.id).filter(Goal.goal_to_study == goal).first()[0]
    teacher_to_study = db.session.query(Teacher).join(TeacherFeatures).join(Goal).filter(
        TeacherFeatures.goal_id == query_gol_id).all()

    return render_template('goal.html', goals=goals_list, teachers=teacher_to_study)


@app.route('/profiles/<int:id>/')
def render_profiles(id):
    teacher = db.session.query(Teacher).get_or_404(id)
    with open('data/teachers.json', 'r', encoding='utf-8') as r:
        teacher_time = json.load(r)
    free_time = teacher_time[id]['free']

    return render_template('profile.html', teacher=teacher, free_time=free_time)


@app.route('/request/', methods=['GET', 'POST'])
def render_request():
    form = app_form.RequestForm()
    if request.method == 'POST' and form.validate_on_submit():
        goal = form.goals.data
        time = form.times.data
        name = form.name.data
        phone = form.phone.data
        request_for_study = Request(goal=goal, free_time=time, student_name=name, student_phone=phone)
        db.session.add(request_for_study)
        db.session.commit()
        return render_template('request_done.html', form=form, goal=goal, time=time, name=name, phone=phone)
    else:
        goals = form.goals
        times = form.times
        return render_template('request.html', form=form, goals=goals, times=times)


@app.route('/booking/<int:id>/<day>/<time>/', methods=['GET', 'POST'])
def render_form(id, day, time):
    form = app_form.BookingForm(clientTime=time, clientWeekday=day)
    teacher = db.session.query(Teacher).get(id)
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        phone = form.phone.data
        time = form.clientTime.data
        day = form.clientWeekday.data
        teacher_id = form.clientTeacher.data
        student = Student(student_name=name, student_phone=phone)
        db.session.add(student)
        db.session.commit()
        booking = Booking(teacher_id=teacher_id, student_id=student.id, study_day=day, study_time=time)
        db.session.add(booking)
        db.session.commit()
        return render_template('booking_done.html', name=name, phone=phone, day=day, time=time)
    else:
        return render_template('booking.html', form=form, day=day, time=time, teacher=teacher, id=teacher.id)


if __name__ == '__main__':
    app.run()
