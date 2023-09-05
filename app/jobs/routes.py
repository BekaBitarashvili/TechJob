from flask import render_template, request, Blueprint, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from app import db
from app.models import Job
from app.jobs.forms import JobForm

jobs = Blueprint('jobs', __name__)


@jobs.route('/job/new', methods=['POST', 'GET'])
@login_required
def new_job():
    form = JobForm()
    if form.validate_on_submit():
        job = Job(title=form.title.data, description=form.description.data, salary=form.salary.data,
                  location=form.location.data, benefits=form.benefits.data,
                  data_verification=form.data_verification.data, required_skills=form.required_skills.data,
                  author=current_user)
        db.session.add(job)
        db.session.commit()
        flash('ვაკანსია წარმატებით შეიქმნა!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_job.html', title='ახალი ვაკანსია', legend='ახალი ვაკანსია', form=form)


@jobs.route('/job/<int:job_id>')
def job(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('job.html', title=job.title, job=job)


@jobs.route('/job/<int:job_id>/update', methods=['POST', 'GET'])
@login_required
def updatejob(job_id):
    job = Job.query.get_or_404(job_id)
    if job.author != current_user:
        abort(403)
    form = JobForm()
    if form.validate_on_submit():
        job.title = form.title.data
        job.description = form.description.data
        job.salary = form.salary.data
        job.location = form.location.data
        job.benefits = form.benefits.data
        job.data_verification = form.data_verification.data
        job.required_skills = form.required_skills.data
        db.session.commit()
        flash('ვაკანსია წარმატებით განახლდა!', 'success')
        return redirect(url_for('jobs.job', job_id=job.id))
    elif request.method == 'GET':
        form.title.data = job.title
        form.description.data = job.description
        form.salary.data = job.salary
        form.location.data = job.location
        form.benefits.data = job.benefits
        form.data_verification.data = job.data_verification
        form.required_skills.data = job.required_skills
    return render_template('create_job.html', title='Update Job', legend='ვაკანსიის განახლება', form=form)


@jobs.route('/job/<int:job_id>/delete', methods=['POST', 'GET'])
@login_required
def deletejob(job_id):
    job = Job.query.get_or_404(job_id)
    if job.author != current_user:
        abort(403)
    db.session.delete(job)
    db.session.commit()
    flash('ვაკანსია წარმატებით წაიშალა!', 'success')
    return redirect(url_for('main.home'))
