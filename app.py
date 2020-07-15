import json
from flask import Flask, render_template

app = Flask(__name__)

free_days = {
    'mon': 'Понедельник',
    'tue': 'Вторник',
    'wed': 'Среда',
    'thu': 'Четверг',
    'fri': 'Пятница',
    'sat': 'Суббота',
    'sun': 'Воскресенье'
}


@app.route('/')
def render_index():
    return render_template('index.html')


@app.route('/goals/<goal>/')
def render_goals(goal):
    return render_template('goal.html')


@app.route('/profiles/<int:id>/')
def render_profiles(id):
    with open('data/teachers.json', 'r') as f:
        teachers_list = json.load(f)
    teachers_info = teachers_list[id]
    day_info = teachers_info['free']
    return render_template('profile.html', teachers_info=teachers_info, free_days=free_days, day_info=day_info, id=id)


@app.route('/request/')
def render_request():
    return render_template('request.html')


@app.route('/request_done/')
def render_request_done():
    return render_template('request_done.html')


@app.route('/booking/<int:id>/<day>/<time>/')
def render_form(id, day, time):
    return render_template('booking.html')


@app.route('/booking_done/')
def render_booking_done():
    return render_template('booking_done.html')


if __name__ == '__main__':
    app.run()
