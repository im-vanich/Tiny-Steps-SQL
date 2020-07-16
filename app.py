import random
import json
import app_form
from flask import Flask, render_template, request

app = Flask(__name__)
app.secret_key = 'very-Secret-Key'


@app.route('/')
def render_index():
    with open('data/teachers.json', 'r') as f:
        teachers_list = json.load(f)
    teachers_random = random.sample(teachers_list, 6)

    return render_template('index.html', teachers_random=teachers_random)


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
    free_days = {
        'mon': 'Понедельник',
        'tue': 'Вторник',
        'wed': 'Среда',
        'thu': 'Четверг',
        'fri': 'Пятница',
        'sat': 'Суббота',
        'sun': 'Воскресенье'
    }  # dict of weekday  for free days in profile
    with open('data/teachers.json', 'r') as f:
        teachers_list = json.load(f)
    teachers_info = teachers_list[id]
    day_info = teachers_info['free']
    return render_template('profile.html', teachers_info=teachers_info, free_days=free_days, day_info=day_info, id=id)


@app.route('/request/', methods=['GET', 'POST'])
def render_request():
    form = app_form.RequestForm()
    goals = form.goals
    times = form.times
    return render_template('request.html', form=form, goals=goals, times=times)


@app.route('/request_done/', methods=['GET', 'POST'])
def render_request_done():
    with open('data/request.json', 'r', encoding='utf-8') as f:
        request_data = json.load(f)
    if request.method == 'POST':
        form = app_form.RequestForm()
        request_info = {'name': form.name.data,
                        'phone': form.phone.data, 'time': form.times.data, 'goal': form.goals.data}
        request_data.append(request_info)
        with open('data/request.json', 'w', encoding='utf-8') as f:
            json.dump(request_data, f, indent=4, ensure_ascii=False, )
        return render_template('request_done.html', request_info=request_info)
    else:
        return render_template('request.html')


@app.route('/booking/<int:id>/<day>/<time>/', methods=['GET', 'POST'])
def render_form(id, day, time):
    with open('data/teachers.json', 'r') as f:
        teachers_list = json.load(f)
    teachers_info = teachers_list[id]
    day = day
    time = time
    form = app_form.BookingForm(clientTime=time, clientWeekday=day)

    return render_template('booking.html', form=form, teachers_info=teachers_info, day=day, time=time)


@app.route('/booking_done/', methods=['GET', 'POST'])
def render_booking_done():
    with open('data/booking.json', 'r', encoding='utf-8') as f:
        booking_data = json.load(f)
    if request.method == 'POST':
        form = app_form.BookingForm()
        booking_info = {'name': form.name.data, 'phone': form.phone.data, 'day': form.clientWeekday.data,
                        'time': form.clientTime.data}

        booking_data.append(booking_info)

        with open('data/booking.json', 'w', encoding='utf-8') as f:
            json.dump(booking_data, f, indent=4, ensure_ascii=False)
        return render_template('booking_done.html', booking_info=booking_info)
    else:
        return render_template('booking.html')


if __name__ == '__main__':
    app.run()
