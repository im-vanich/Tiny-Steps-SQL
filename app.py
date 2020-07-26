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
    goal_id = db.Column(db.Integer, db.ForeignKey('goals.id'))
    goal = db.relationship('Goal')
    free_time = db.Column(db.String, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    student = db.relationship('Student')


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String, nullable=False, unique=True)
    student_phone = db.Column(db.String, nullable=False, unique=True)
    booking = db.relationship('Booking', back_populates='student')
    request = db.relationship('Request')


class Goal(db.Model):
    __tablename__ = 'goals'

    id = db.Column(db.Integer, primary_key=True)
    goal_to_study = db.Column(db.String, nullable=False)
    db.relationship('Request')
    teachers = db.relationship('Teacher', secondary=teachers_goal)


@app.route('/')
def render_index():
    teacher = db.session.query(Teacher).order_by(Teacher.id).limit(6)
    return render_template('index.html', teachers=teacher)


@app.route('/goals/<goal>/')
def render_goals(goal):
    with open('data/goals.json', 'r', encoding='utf-8') as f:  # read data from goals.json and equal goal info
        goals_data = json.load(f)
    for k, v in goals_data.items():
        if k == goal:
            target = v
    with open('data/teachers.json', 'r') as f:
        teachers_list = json.load(f)
    teachers = []  # create list for teachers in goals
    for teach in teachers_list:
        for k, v in teach.items():
            if k == 'goals':
                if goal in v:
                    teachers.append(teach)

    return render_template('goal.html', target=target, teachers=teachers)


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
    goals = form.goals
    times = form.times
    return render_template('request.html', form=form, goals=goals, times=times)


@app.route('/request_done/', methods=['GET', 'POST'])
def render_request_done():
    form = app_form.RequestForm()
    with open('data/request.json', 'r', encoding='utf-8') as f:
        request_data = json.load(f)
    if request.method == 'POST' and form.validate_on_submit():
        request_info = {'name': form.name.data,
                        'phone': form.phone.data, 'time': form.times.data, 'goal': form.goals.data}
        request_data.append(request_info)
        with open('data/request.json', 'w', encoding='utf-8') as f:
            json.dump(request_data, f, indent=4, ensure_ascii=False, )
        return render_template('request_done.html', request_info=request_info, form=form)
    else:
        return render_template('request.html')


@app.route('/booking/<int:id>/<day>/<time>/', methods=['GET', 'POST'])
def render_form(id, day, time):
    form = app_form.BookingForm(clientTime=time, clientWeekday=day)
    teacher = db.session.query(Teacher).get(id)
    if request.method == 'POST':
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
