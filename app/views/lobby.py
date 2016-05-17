from app import app, models
from flask import Flask, render_template, request
from app.toolbox import email

@app.route("/")
def lobby():
   return render_template('lobby/index.html')

@app.route("/email_test", methods=['POST'])
def email_test():

   html = render_template('email/bet_accepted.html', author_email="jimmymowschess@gmail.com", acceptor_email="jacksonlinechess@gmail.com", wager_link="http://116c0707.ngrok.io/wager/56e18829")
   email.send_email(["jimmymowschess@gmail.com"], "Your bet has been accepted on Zero House Edge", html)
   return "success"

