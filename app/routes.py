from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm
from app.models import User, Job
from flask_login import login_user, current_user, logout_user, login_required

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
    },
    {
        'author': 'Oracle',
        'title': 'JavaScript Developer',
        'content': 'JavaScript is awesome, and React is even more awesome!, Sixth post content,',
        'date_posted': 'April 25, 2020'
    },
    {
        'author': 'IBM',
        'title': 'PHP Developer',
        'content': 'PHP is awesome, and Laravel is even more awesome!, Seventh post content,',
        'date_posted': 'April 26, 2020'
    },
    {
        'author': 'Intel',
        'title': 'Ruby Developer',
        'content': 'Ruby is awesome, and Rails is even more awesome!, Eighth post content,',
        'date_posted': 'April 27, 2020'
    },
    {
        'author': 'Twitter',
        'title': 'Go Developer',
        'content': 'Go is awesome, and Gin is even more awesome!, Ninth post content,',
        'date_posted': 'April 28, 2020'
    },
    {
        'author': 'Uber',
        'title': 'Rust Developer',
        'content': 'Rust is awesome, and Rocket is even more awesome!, Tenth post content,',
        'date_posted': 'April 29, 2020'
    },
    {
        'author': 'Netflix',
        'title': 'Kotlin Developer',
        'content': 'Kotlin is awesome, and Ktor is even more awesome!, Eleventh post content,',
        'date_posted': 'April 30, 2020'
    },
    {
        'author': 'Airbnb',
        'title': 'Dart Developer',
        'content': 'Dart is awesome, and Flutter is even more awesome!, Twelfth post content,',
        'date_posted': 'May 1, 2020'
    },
    {
        'author': 'Paypal',
        'title': 'TypeScript Developer',
        'content': 'TypeScript is awesome, and Angular is even more awesome!, Thirteenth post content,',
        'date_posted': 'May 2, 2020'
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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your Account has been created! Now Log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account')
@login_required
def account():
    form = UpdateAccountForm()
    image_file = url_for('static', filename='images/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)
