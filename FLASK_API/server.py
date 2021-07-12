# -*- coding: utf-8 -*-

from flask import Flask, url_for, request, render_template, redirect
from data import Data
from model import Model
from orm import dbsession
from orm.users import User
from flask_login import LoginManager, login_manager, login_user, current_user
from arg_parser import terminal_arguments

app = Flask(__name__)
app.secret_key = "super secret key"
login_manager = LoginManager()
data = Data()
model = None
login_flag = False
email = ''
password = ''
user_name = 'default'


@login_manager.user_loader
def load_user(user_id):
    db_sess = dbsession.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Регистрация пользователя"""

    if request.method == 'GET':
        return render_template('register.html', style_path=url_for('static', filename='css/style.css'))
    elif request.method == 'POST':
        db_sess = dbsession.create_session()

        # Проверка пользователя по почте
        if db_sess.query(User).filter(User.email == request.form.get('email')).first():
            return 'Пользователь уже существует'

        # Получение данных пользователя
        name = request.form.get('name')
        email = request.form.get('email')
        pswd = request.form.get('password')
        # Заполнить все поля
        if not (name and email and pswd):
            return 'Заполните все поля'

        # Инициализация пользователя и запись в базе
        user = User(
            name=name,
            email=email
        )
        user.set_password(pswd)
        db_sess.add(user)
        db_sess.commit()

        # Автоматическая авторизация
        login(email, pswd)

        return redirect('/form')


def process(question):
    """Обработать вопрос пользователя и выдать ответ"""
    model.set_question(question)
    return model.get_answer()


@app.route('/form', methods=['POST', 'GET'])
def form_sample():
    """Форма 'общения' НС с пользователем, содержащая поля текста, вопроса, ответа..."""

    if request.method == 'GET':
        data.set_text(model.get_text())  # Установить значение поля 'текст'
        data.set_question(model.get_question())  # Установить значения поля 'вопрос'
        return render_template('index.html', style_path=url_for('static', filename='css/style.css'),
                               text=data.get_text(), question=data.get_question(), answer=data.get_answer(),
                               user_name=user_name)
    elif request.method == 'POST':
        data.set_question(request.form.get('question'))  # Получить значение поля 'вопрос' и установить
        if request.form.get('accept'):
            # Если выбрана обработка текста
            data.set_text(request.form.get('text'))
            model.set_text(data.get_text())
            print('accept')
        data.set_answer(process(data.get_question()))  # Получить ответ на вопрос
        return render_template('index.html', style_path=url_for('static', filename='css/style.css'),
                               text=data.get_text(), question=data.get_question(), answer=data.get_answer(),
                               user_name=user_name)


@app.route('/')
def index():
    global email
    global password

    if login_flag:
        # Авторизация пользователя и перенаправление на форму
        login(email, password)
        return redirect('/form')

    # Перенаправить на форму регистрации
    return redirect('/register')


def login(email, password):
    """Вход в систему (авторизация пользователя) с указанными почтой и паролем"""

    global user_name

    db_sess = dbsession.create_session()
    user = db_sess.query(User).filter(User.email == email).first()  # Выявить пользователя по почте

    # Проверить пароль
    if user and user.check_password(password):
        login_user(user, remember=True)
        user_name = current_user.name  # Выставить текущего пользователя
        return True
    return False


def main():
    dbsession.global_init('db/account.db')
    login_manager.init_app(app)

    # Объявление необходимых глобальных переменных
    global login_flag
    global model
    global email
    global password

    args_dict = terminal_arguments()  # Получить аргументы командной строки

    # В зависимости от того, первый раз запускается программа
    if args_dict['first_run']:
        model = Model(download=True)  # Инициализация НС путем скачивания предобученной модели
    else:
        model = Model(download=False)  # Инициализация НС загруженной моделью

    # Указаны почта и пароль
    if args_dict['email'] and args_dict['password']:
        email = args_dict['email']
        password = args_dict['password']
        login_flag = not login_flag
        print('login_flag', login_flag)
    # Указан файл с почтой и паролем
    elif args_dict['config']:
        email = args_dict['config'][0]
        password = args_dict['config'][1]
        login_flag = not login_flag
        print('login_flag', login_flag)
    # Не указан флаг регистрации
    elif not args_dict['register']:
        return 'Нет доступа'

    # Указан флаг регистрации
    if args_dict['register']:
        login_flag = False

    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
