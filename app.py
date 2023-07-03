from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asndaiusdjaosid83459347593475asjdaisd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(30), nullable=False)
    jobs = db.relationship('Job', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), unique=True, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Job('{self.title}', '{self.date_posted}')"


def create_database():
    with app.app_context():
        db.create_all()


jobs = [
    {
        'author': 'Google',
        'title': 'Python Developer',
        'content': 'Python is awesome, and Flask is even more awesome!, First post content,',
        'date_posted': 'April 20, 2020'
    },
    {
        'author': 'Facebook',
        'title': 'Java Developer',
        'content': 'Java is awesome, and Spring is even more awesome!, Second post content,',
        'date_posted': 'April 21, 2020'
    },
    {
        'author': 'Amazon',
        'title': 'C++ Developer',
        'content': 'C++ is awesome, and Django is even more awesome!, Third post content,',
        'date_posted': 'April 22, 2020'
    },
    {
        'author': 'Microsoft',
        'title': 'C# Developer',
        'content': 'C# is awesome, and ASP.NET is even more awesome!, Fourth post content,',
        'date_posted': 'April 23, 2020'
    },
    {
        'author': 'Apple',
        'title': 'Swift Developer',
        'content': 'Swift is awesome, and SwiftUI is even more awesome!, Fifth post content,',
        'date_posted': 'April 24, 2020'
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', jobs=jobs)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@gmail.com' and form.password.data == 'password':
            flash(f'You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)


if __name__ == '__main__':
    create_database()
    app.run(debug=True)
