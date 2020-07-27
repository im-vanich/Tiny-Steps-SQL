from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField, RadioField
from wtforms.validators import InputRequired, Length


class BookingForm(FlaskForm):
    name = StringField('Вас зовут', [InputRequired(message='Введите корректное имя'), Length(min=2, max=30)])
    phone = StringField('Ваш телефон', [InputRequired(message='Введите корректный номер телефона'), Length(min=6, max=12)])
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
    name = StringField('Вас зовут', [InputRequired(message='Введите корректное имя'), Length(min=2, max=30)])
    phone = StringField('Ваш телефон', [InputRequired(message='Введите корректный номер телефона'), Length(min=6, max=12)])
    submit = SubmitField('Найдите мне преподавателя')
