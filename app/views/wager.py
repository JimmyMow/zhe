from flask import Blueprint, render_template, url_for, Response, stream_with_context, request
from app import app, models, db
from app.toolbox import mlb
from datetime import datetime
from math import sqrt
import time
import json

# Create a wager blueprint
wagerbp = Blueprint('wagerbp', __name__, url_prefix='/wager')

@wagerbp.route('', methods=['GET'])
def all_wagers():
    wagers = models.MLBWager.query.all()
    return render_template('wager/all.html', wagers=wagers)

@wagerbp.route('/<path:wager_id>', methods=['GET', 'POST'])
def wager(wager_id):
  wager = models.MLBWager.query.filter_by(id=wager_id).first()

  if request.method == 'POST':
    def create_contract(wager):
        if wager.away_id:
          msg = "home needs to be claimed"
        elif wager.home_id:
          msg = "away needs to be claimed"
        else:
          abort(500)

        for x in range(5):
          yield msg
          time.sleep(2) # an artificial delay

    return Response(create_contract(wager), content_type='text/event-stream')

  game = mlb.get_mlb_game(wager.game_id)
  return render_template('wager/show.html', wager=wager, game=game, innings=[])

@wagerbp.route('/<path:wager_id>/stream_events', methods=['GET'])
def stream_events(wager_id):
   wager = models.MLBWager.query.filter_by(id=wager_id).first()
   def generate(wager):
      events = mlb.get_game_events(wager.game_id)
      res = json.dumps(events['html']['body']['game']['inning'])

      yield res

   return app.response_class(generate(wager), mimetype='application/json')
