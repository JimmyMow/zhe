from threading import Thread
from flask.ext.mail import Message
from app import app, mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(recipients, subject, html_body):
    sender = app.config['ADMINS'][0]
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.html = html_body
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
