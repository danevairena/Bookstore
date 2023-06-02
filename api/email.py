from flask_mail import Message

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

