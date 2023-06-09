from flask_mail import Message
from flask import render_template
from api import mail, app
# support for running asynchronous tasks by threading
from threading import Thread


# The send_async_email function now runs in a background thread, invoked via the Thread class,
# so that the application can continue running concurrently with the email being sent.
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

# Email sending wrapper function.
def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()

# Send password reset email function.
def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[Bookstore] Reset Your Password',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('reset_password.html',
                                         user=user, token=token))