import json
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField, RadioField
from wtforms.validators import InputRequired, Length

app = Flask(__name__)
app.secret_key = 'very-Secreat_Key'


class BookingForm(FlaskForm):
    name = StringField('Вас зовут', [InputRequired(), Length(min=2, max=30)])
    phone = StringField('Ваш телефон', [InputRequired(), Length(min=6, max=12)])
    clientWeekday = HiddenField('clientWeekday', default='mon')
    clientTime = HiddenField('clientTime', default='12:00')
    clientTeacher = HiddenField('clientTeacher', default='10')
    submit = SubmitField('Записаться на пробный урок')


class RequestForm(FlaskForm):
    goals = RadioField('Какая цель занятий?',
                       choices=[('Для путешествий', 'Для путешествий'), ('Для школы', 'Для школы'),
                                ('Для работы', 'Для работы'),
                                ('Для переезда', 'Для переезда')])
    times = RadioField('Сколько времени есть?', choices=[('1-2 часа в неделю', '1-2 часа в неделю'),
                                                         ('3-5 часов в неделю', '3-5 часов в неделю'),
                                                         ('5-7 часов в неделю', '5-7 часов в неделю'),
                                                         ('7-10 часов в неделю', '7-10 часов в неделю')])
    name = StringField('Вас зовут', [InputRequired(), Length(min=2, max=30)])
    phone = StringField('Ваш телефон', [InputRequired(), Length(min=6, max=12)])
    submit = SubmitField('Найдите мне преподавателя')


@app.route('/')
def render_index():
    return render_template('index.html')


@app.route('/goals/<goal>/')
def render_goals(goal):
    return render_template('goal.html')


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
    }  # dict of day week for free days in profile
    with open('data/teachers.json', 'r') as f:
        teachers_list = json.load(f)
    teachers_info = teachers_list[id]
    day_info = teachers_info['free']
    return render_template('profile.html', teachers_info=teachers_info, free_days=free_days, day_info=day_info, id=id)


@app.route('/request/', methods=['GET', 'POST'])
def render_request():
    form = RequestForm()
    goals = form.goals
    times = form.times
    return render_template('request.html', form=form, goals=goals, times=times)


@app.route('/request_done/', methods=['GET', 'POST'])
def render_request_done():
    with open('data/request.json', 'r', encoding='utf-8') as f:
        request_data = json.load(f)
    if request.method == 'POST':
        form = RequestForm()
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
    form = BookingForm(clientTime=time, clientWeekday=day)

    return render_template('booking.html', form=form, teachers_info=teachers_info, day=day, time=time)


@app.route('/booking_done/', methods=['GET', 'POST'])
def render_booking_done():
    with open('data/booking.json', 'r', encoding='utf-8') as f:
        booking_data = json.load(f)
    if request.method == 'POST':
        form = BookingForm()
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
