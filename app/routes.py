import os
import secrets
from flask import render_template, url_for, flash, redirect, request, abort
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, JobForm
from app.models import User, Job
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    jobs = Job.query.order_by(Job.date_posted.desc()).paginate(page=page, per_page=10)
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


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)
    form_picture.save(picture_path)
    # return picture_fn
    # picture_fn = random_hex + f_ext
    # picture_path = os.path.join(app.root_path, 'static/images', picture_fn)
    # i = Image.open(form_picture)
    # i.thumbnail((125, 125))
    # i.save(picture_path)
    return picture_fn


@app.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        # db.session.add(user)
        db.session.commit()
        flash('Your Account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='images/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route('/job/new', methods=['POST', 'GET'])
@login_required
def new_job():
    form = JobForm()
    if form.validate_on_submit():
        job = Job(title=form.title.data, description=form.description.data, author=current_user)
        db.session.add(job)
        db.session.commit()
        flash('Your Job has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_job.html', title='New Job', legend='New Job', form=form)


@app.route('/job/<int:job_id>')
def job(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('job.html', title=job.title, job=job)


@app.route('/job/<int:job_id>/update', methods=['POST', 'GET'])
@login_required
def updatejob(job_id):
    job = Job.query.get_or_404(job_id)
    if job.author != current_user:
        abort(403)
    form = JobForm()
    if form.validate_on_submit():
        job.title = form.title.data
        job.description = form.description.data
        db.session.commit()
        flash('Your Job has been updated!', 'success')
        return redirect(url_for('job', job_id=job.id))
    elif request.method == 'GET':
        form.title.data = job.title
        form.description.data = job.description
    return render_template('create_job.html', title='Update Job', legend='Update Job', form=form)


@app.route('/job/<int:job_id>/delete', methods=['POST', 'GET'])
@login_required
def deletejob(job_id):
    job = Job.query.get_or_404(job_id)
    if job.author != current_user:
        abort(403)
    db.session.delete(job)
    db.session.commit()
    flash('Your Job has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route('/user/<string:username>')
def user_jobs(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    jobs = Job.query.filter_by(author=user).order_by(Job.date_posted.desc()).paginate(page=page, per_page=10)
    return render_template('user_jobs.html', jobs=jobs, user=user)
