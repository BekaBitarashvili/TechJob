from flask import render_template, request, Blueprint
from app.models import Job

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    jobs = Job.query.order_by(Job.date_posted.desc()).paginate(page=page, per_page=10)
    return render_template('home.html', jobs=jobs)


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/search')
def search():
    query = request.args.get('query')
    results = Job.query.filter(Job.title.ilike(f'%{query}%')).all()
    return render_template('search.html', results=results)
