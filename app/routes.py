from flask import render_template, flash, redirect, url_for, session
from app import app
from app.forms import LoginForm, ConnectForm, ConvertForm
from db import Connection, get_db, close_db, connect_db


@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, host {}, db {}, remember_me={}'.format(
            form.username.data, form.host.data, form.db.data, form.remember_me.data))
        conn = connect_db(form.host.data, form.db.data, form.username.data, form.password.data)
        return redirect(url_for('convert'))

    return render_template('login.html',  title='Sign In', form=form)


@app.route('/', methods=['GET', 'POST'])
@app.route('/connect', methods=['GET', 'POST'])
def connect():
    form = ConnectForm()
    if form.validate_on_submit():
        conn = connect_db(form.server.data, form.db.data, form.username.data, form.password.data)
        if conn.error:
            flash('Connection Error {}'.format(conn.error))
            render_template('connect-form.html', title='Connect to The Database', connError="hi-error", form=form)
        else:
            flash('Connected successfully to the database')
            return redirect(url_for('convert'))
    return render_template('connect-form.html', title='Connect to The Database', form=form)


@app.route('/convert', methods=['GET', 'POST'])
def convert():
    form = ConvertForm()
    if form.validate_on_submit():
        conn = get_db()
        result = conn.run_via_cursor(form.text.data)
        
        if isinstance(result, str):
            # error happend executing sql query
            flash('Convert From requested text {}'.format(result))
            return render_template('convert-form.html',  title='Enter the text to convert into SQL', form=form)

        columns = [column[0] for column in result.description]
        rows = result.fetchall()

        # if conn is none redirect to /login
        flash('Convert From requested text {}'.format(form.text.data))

        return render_template('table2.html',  title='Enter the text to convert into SQL', rows=rows, columns=columns)

    return render_template('convert-form.html',  title='Enter the text to convert into SQL', form=form)



@app.route('/table', methods=['GET', 'POST'])
def table():
    return render_template('table.html',  title='Enter the text to convert into SQL', data={})

