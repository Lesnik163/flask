from extensions import db

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    text = db.Column(db.Text, nullable=False)
    subtitle = db.Column(db.String(100), nullable=True)