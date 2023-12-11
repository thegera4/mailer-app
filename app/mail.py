from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, current_app
)
from app.db import get_db
import sendgrid
from sendgrid.helpers.mail import *

bp = Blueprint('mail', __name__, url_prefix='/')


@bp.route('/', methods=['GET'])
def index():
    search = request.args.get('search')
    db, c = get_db()

    if not search:
        c.execute('SELECT * FROM email')
    else:
        c.execute('SELECT * FROM email WHERE content LIKE %s', ('%' + search + '%',))

    mails = c.fetchall()
    return render_template('mails/index.html', mails=mails)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        email = request.form.get('email')
        subject = request.form.get('subject')
        content = request.form.get('content')

        errors = []
        if not email:
            errors.append('Email is required.')
        if not subject:
            errors.append('Subject is required.')
        if not content:
            errors.append('Content is required.')

        if len(errors) == 0:
            send_email(email, subject, content)
            db, c = get_db()
            c.execute('INSERT INTO email (email, subject, content) VALUES (%s, %s, %s)', (email, subject, content))
            db.commit()
            return redirect(url_for('mail.index'))
        else:
            for error in errors:
                flash(error)

    return render_template('mails/create.html')


def send_email(sender_email, email_subject, message_content):
    sg = sendgrid.SendGridAPIClient(api_key=current_app.config['SENDGRID_KEY'])
    sender = Email(current_app.config['FROM_EMAIL'])
    receiver = To(sender_email)
    body = Content("text/plain", message_content)
    whole_mail = Mail(sender, receiver, email_subject, body)
    response = sg.client.mail.send.post(request_body=whole_mail.get())
    print(response)
