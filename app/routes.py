from flask import render_template, url_for, flash, redirect
from app import app
from app.forms import RegistrationForm, LoginForm
from app.models import User, Job

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