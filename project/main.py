from flask import Flask, render_template, request

app = Flask(__name__)
diary = {}

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
            diary[note_title] = note_content
    title = 'Дневник программиста'
    return render_template('notes.html', title=title, notes=diary)

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html', 404)

if __name__ == '__main__':
    app.run(debug=True)