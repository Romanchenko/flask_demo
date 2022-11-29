#https://flask.palletsprojects.com/en/2.2.x/quickstart/#rendering-templates

import os

from flask import Flask, session, escape, redirect, url_for, abort, flash, send_file
from flask import render_template
from flask import request, g

from storage import get_db, init_db

app = Flask(__name__)

@app.teardown_appcontext  # декоратор при разрыве connection
def close_db(error):  # закрытие может проходить как нормально, так и с ошибкой, которую можно обрабатывать
    """Закрываем БД при разрыве"""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"


@app.route('/user/<username>')  # переменные задаются через <>
def show_user_profile(username):
    return 'User %s' % username


@app.route('/post/<int:post_id>')  # отдельно можем задать ограничение на тип (например, здесь указываем int)
def show_post(post_id):
    return 'Post %d' % post_id

# ya.ru/search?text=abacaba
@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(
            session['username'])  # escape заменяет все специсимволы на безопасные (потому что можно же ломать сайты)
    return 'You are not logged in'


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['logged_in'] = True
        return redirect(url_for('index'))
    db = get_db(app.config['DATABASE'])
    cur = db.execute('select title, text from entries order by id desc')
    entries = [x for x in cur.fetchall()]
    return render_template('login.html', entries=entries)
    # '''
    # <form action="" method="post">
    # <p><input type=text name=username>
    # <p><input type=submit value=Login> </form>
    # '''


@app.route('/logout')
def logout():
    # удалить из сессии имя пользователя, если оно там есть
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/entries')
def show_entries():
    title = request.args.get('title')
    db = get_db(app.config['DATABASE'])
    author = session['username']
    if title is None:
        query = f'select title, text, author from entries where author = \'{author}\' order by id desc'
    else:
        query = f'select title, text from entries where title = \'{title}\' and author = \'{author}\' order by id desc'
    cur = db.execute(query)
    entries = cur.fetchall()
    return render_template('show_entities.html', entries=entries)


@app.before_request
def preprocess():
    print('preprocess called')


@app.teardown_request
def tear_down_r(err):
    print('tear down called')
    pass


@app.route('/pic', methods=['GET'])
def send_pic():
    return send_file('static/meme.png', mimetype='image/gif')


@app.route('/add', methods=['GET', 'POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    if request.method == 'GET':
        return '''
        <form action="" method="post">
        <p><input type=text name=title>
        <p><input type=text name=text>
        <p><input type=submit value=ADD> </form>
        '''
    print(app.config)
    db = get_db(app.config['DATABASE'])
    author = session['username']
    db.execute(
        'insert into entries (title, text, author) values (?, ?, ?)',
        [request.form['title'], request.form['text'], author]
    )
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'  # секретный ключ (а зачем он? А чтобы пользователь куки не менял)

# if __name__ == '__main__':
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, '../flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'))
init_db(app, app.config['DATABASE'])
print('XXX', app.config)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.run(debug=True)
