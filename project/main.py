import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

load_dotenv(Path(__file__).resolve().parents[1] / '.env')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
db = SQLAlchemy(app)
migrate = Migrate(app, db)
class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    text = db.Column(db.Text, nullable=False)
    subtitle = db.Column(db.String(100), nullable=True)

@app.route('/')
def index():
    title = 'Главная'
    return render_template('home.html', title=title)

@app.route('/blog')
def blog():
    title = 'Блог'
    return render_template('blog.html', title=title)

@app.route('/notes', methods=['GET', 'POST'])
def notes():
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