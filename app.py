import os

import markdown2
from markdown2 import Markdown
from flask import Flask, render_template, request, session, make_response, redirect, url_for

app = Flask(__name__)
app.secret_key = os.urandom(24)
markdowner = Markdown()


@app.route('/')
def index():
    return render_template('index.html')


@app.context_processor
def inject_organization_name():
    return dict(organization_name="БУЗ ВО ВГКП №3")


@app.route('/schedule')
def schedule():
    # Получаем выбранные отделение и корпус из cookies
    selected_department = request.cookies.get('department', '')
    selected_building = request.cookies.get('building', '')

    # Пример данных расписания
    schedule_data = [
        {'doctor': 'Иванов Иван Иванович', 'specialty': 'Терапевт', 'department': 'Кардиология', 'today_slots': 3,
         'next_14_days': 10},
        {'doctor': 'Петров Петр Петрович', 'specialty': 'Хирург', 'department': 'Хирургия', 'today_slots': 5,
         'next_14_days': 12},
        {'doctor': 'Сидорова Светлана Сидоровна', 'specialty': 'Кардиолог', 'department': 'Кардиология',
         'today_slots': 2, 'next_14_days': 8},
    ]

    # Фильтрация по отделению
    if selected_department:
        schedule_data = [item for item in schedule_data if item['department'] == selected_department]

    return render_template('schedule.html', schedule=schedule_data, selected_department=selected_department,
                           selected_building=selected_building)


@app.route('/specialty/<specialty>')
def specialty_description(specialty):
    # Описание для каждой специальности
    descriptions = {
        'Терапевт': '''
        **Врач-терапевт** — специалист, занимающийся диагностикой, лечением и профилактикой широкого спектра заболеваний внутренних органов.
        Основные обязанности врача-терапевта включают...
        ''',
        'Кардиолог': '''
        **Кардиолог** — специалист, занимающийся диагностикой и лечением заболеваний сердечно-сосудистой системы.
        Основные обязанности кардиолога включают...
        ''',
        'Хирург': '''
        **Хирург** — врач, который выполняет хирургические операции для лечения различных заболеваний и травм.
        Основные обязанности хирурга включают...
        '''
    }

    description = descriptions.get(specialty, 'Описание не найдено.')
    description_html = markdowner.convert(description)

    return render_template('specialty.html', specialty=specialty, description=description_html)


@app.route('/specialties')
def specialties():
    specialties_list = ['Терапевт', 'Кардиолог', 'Хирург']
    return render_template('specialties.html', specialties=specialties_list)


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'authenticated' not in session:
        return redirect(url_for('settings_auth'))

    if request.method == 'POST':
        # Сохранение настроек
        building = request.form.get('building')
        department = request.form.get('department')
        color_scheme = request.form.get('color_scheme')

        resp = make_response(redirect(url_for('index')))
        resp.set_cookie('building', building)
        resp.set_cookie('department', department)
        resp.set_cookie('color_scheme', color_scheme)

        # Сброс аутентификации после сохранения
        session.pop('authenticated', None)
        return resp

    # Получение текущих настроек из cookies
    building = request.cookies.get('building', '')
    department = request.cookies.get('department', '')
    color_scheme = request.cookies.get('color_scheme', 'default')

    return render_template('settings.html', building=building, department=department, color_scheme=color_scheme)


@app.route('/settings/auth', methods=['GET', 'POST'])
def settings_auth():
    if request.method == 'POST':
        pin = request.form.get('pin')
        if pin == '1234':  # Установите ваш пин-код
            session['authenticated'] = True
            return redirect(url_for('settings'))
        else:
            error = 'Неверный пин-код. Попробуйте снова.'
            return render_template('settings_auth.html', error=error)
    return render_template('settings_auth.html')


if __name__ == '__main__':
    app.run(debug=True, port=5020)
