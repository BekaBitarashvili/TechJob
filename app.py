from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'asndaiusdjaosid83459347593475asjdaisd'

jobs = [
    {
        'author': 'Google',
        'title': 'Python Developer',
        'content': 'Python is awesome, and Flask is even more awesome!, First post content,',
        'date_posted': 'April 20, 2020'
    },
    {
        'author': 'Facebook',
        'title': 'Blog Post 2',
        'content': 'Selenium is awesome, and Flask is even more awesome!, Second post content,',
        'date_posted': 'April 21, 2021'
    },
    {
        'author': 'Facebook',
        'title': 'Blog Post 2',
        'content': 'Selenium is awesome, and Flask is even more awesome!, Second post content,',
        'date_posted': 'April 21, 2021'
    },
    {
        'author': 'Facebook',
        'title': 'Blog Post 2',
        'content': 'Selenium is awesome, and Flask is even more awesome!, Second post content,',
        'date_posted': 'April 21, 2021'
    },
    {
        'author': 'Facebook',
        'title': 'Blog Post 2',
        'content': 'Selenium is awesome, and Flask is even more awesome!, Second post content,',
        'date_posted': 'April 21, 2021'
    },
    {
        'author': 'Facebook',
        'title': 'Blog Post 2',
        'content': 'Selenium is awesome, and Flask is even more awesome!, Second post content,',
        'date_posted': 'April 21, 2021'
    },
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
    app.run(debug=True)
