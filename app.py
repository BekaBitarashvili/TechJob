from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'asndaiusdjaosid83459347593475asjdaisd'

posts = [
    {
        'author': 'Nishant',
        'title': 'Python Developer',
        'content': 'Python is awesome, and Flask is even more awesome!, First post content,',
        'date_posted': 'April 20, 2020'
    },
    {
        'author': 'Nishant',
        'title': 'Blog Post 2',
        'content': 'Selenium is awesome, and Flask is even more awesome!, Second post content,',
        'date_posted': 'April 21, 2020'
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    return render_template('register.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
