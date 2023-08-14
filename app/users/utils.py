import os
import secrets
from flask import url_for
from flask import current_app as app
from flask_mail import Message
from app import db, mail


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


def send_mail(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', recipients=[user.email], sender='noreply@demo.com')
    msg.body = f'''To reset your password, visit the following link:

{url_for('users.reset_token', token=token, _external=True)}
    '''
