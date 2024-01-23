# Задание (семинар 3)
# Создать форму для регистрации пользователей на сайте. 
# Форма должна содержать поля "Имя", "Фамилия", "Email", "Пароль" и кнопку "Зарегистрироваться". 
# При отправке формы данные должны сохраняться в базе данных, а пароль должен быть зашифрован.

# Сделано, используя код с семинара

from flask import Flask, render_template, request, url_for
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash # функция для шифрования
from forms import RegistrationForm
from models import User, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mybase.db'
db.init_app(app)
migrate = Migrate(app, db)

app.config['SECRET_KEY'] = b'9ee517a911895b1afa068c62036386ff9289c2ff544ee2f5c60e7e85451d3176'
csrf = CSRFProtect(app)


@app.context_processor
def menu_items():
    menu_items = [
        {'name': 'Home', 'url': url_for("index")},
        {'name': 'Registration', 'url': url_for("registration")},
    ]
    return dict(menu_items=menu_items)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    context = {'alert_message': "Добро пожаловать!"}
    form = RegistrationForm()
    name = form.name.data
    surname = form.surname.data
    email = form.email.data
    password = form.password.data
    terms = form.terms.data
    if request.method == 'POST' and form.validate():
        if User.query.filter(User.email == email).all():
            context = {'alert_message': "Пользователь уже существует!"}
            return render_template('registration.html', form=form, **context)
        else:
            hashed_password = generate_password_hash(form.password.data) # шифруем пароль
            new_user = User(name=name, surname=surname, email=email, password=hashed_password, terms=terms)
            db.session.add(new_user)
            db.session.commit()
            context = {'alert_message': "Пользователь добавлен!"}
            return render_template('registration.html', form=form, **context)
    return render_template('registration.html', form=form)
