from flask import Flask, render_template, request, make_response, redirect, url_for

app = Flask(__name__)

@app.context_processor
def inject_menu_items():
    menu_items = [
        {'url': '/', 'name': 'Главная'},
        {'url': '/about', 'name': 'О нас'},
        {'url': '/contact', 'name': 'Контакты'}
    ]
    return dict(menu_items=menu_items)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']

        # создаём cookie-файл с данными пользователя
        resp = make_response(redirect(url_for('welcome')))
        resp.set_cookie('user_data', f'{username}::{email}')
        return resp
    return render_template('index.html')

@app.route('/welcome')
def welcome():
    # получаем данные из cookie-файла
    user_data = request.cookies.get('user_data')
    if not user_data:
        return redirect(url_for('index'))
    username, _ = user_data.split('::')

    return render_template('welcome.html', username=username)

@app.route('/logout')
def logout():
    # удаляем cookie-файл
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('user_data', expires=0)
    return resp

if __name__ == '__main__':
    app.run(debug=True)