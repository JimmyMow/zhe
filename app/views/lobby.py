from app import app, models
from flask import Flask, render_template, request
from app.toolbox import email

@app.route("/")
def lobby():
   return render_template('lobby/index.html')


