from app import app, models
from flask import Flask, render_template, request

@app.route("/")
def lobby():
   # mlb_wagers = models.MLBWager.query.all()
   return render_template('lobby/index.html')

