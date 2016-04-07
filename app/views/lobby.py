from app import app, models
from flask import Flask, render_template, request

@app.route("/")
def lobby():
   mlb_wagers = models.MLBWager.query.all()
   print("wagers: {}".format(mlb_wagers))
   return render_template('lobby/index.html', mlb_wagers=mlb_wagers)

