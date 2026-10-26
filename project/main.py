import os
from pathlib import Path
import secrets

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session

from extensions import db, migrate
from models import Notes, Users

from datetime import datetime, timedelta, timezone

load_dotenv(Path(__file__).resolve().parents[1] / '.env')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
db.init_app(app)
migrate.init_app(app, db)


def active_user():
    token = session.get('token')
    user = None
    if token:
        user = db.session.query(Users).filter_by(token=token).first()
    if (
        user is None
        or user.token_expires is None
        or user.token_expires < datetime.now(timezone.utc)
    ):
        session.pop('token', None)
        return None
    return user


@app.route('/home')
def index():
    title = 'Главная'
    return render_template('home.html', title=title)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '')
        email = request.form.get('email', '')
        password = request.form.get('password', '')
        if username and email and password:
            token = secrets.token_hex(16)
            token_expires = datetime.now(timezone.utc) + timedelta(hours=1)
            user = Users(username=username, email=email, password=password, token=token, token_expires=token_expires)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))

    title = 'Регистрация'
    return render_template('register.html', title=title)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        user = db.session.query(Users).filter_by(username=username, password=password).first()
        if user:
            user.token = secrets.token_hex(16)
            user.token_expires = datetime.now(timezone.utc) + timedelta(hours=1)
            db.session.commit()
            session['token'] = user.token
            return redirect(url_for('notes'))

    title = 'Вход'
    return render_template('login.html', title=title)

@app.route('/blog')
def blog():
    if active_user() is None:
        return redirect(url_for('login'))
    title = 'Блог'
    return render_template('blog.html', title=title)

@app.route('/notes', methods=['GET', 'POST'])
def notes():
    if active_user() is None:
        return redirect(url_for('login'))

    if request.method == 'POST':
        note_title = request.form.get('title', '')
        note_content = request.form.get('content', '')
        if note_title:
            note = Notes(title=note_title, text=note_content)
            db.session.add(note)
            db.session.commit()
            return redirect(url_for('notes'))
    notes = db.session.query(Notes).all()      
    title = 'Дневник программиста'
    return render_template('notes.html', title=title, notes=notes)

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html', 404)

if __name__ == '__main__':
    app.run(debug=True)