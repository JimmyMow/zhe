from flask import Blueprint, render_template, url_for, Response, stream_with_context, request, abort, session
from app import app, models, db

from app.toolbox import mlb
from app.toolbox.wallet_helper import wallet_helper

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
    try:
      user_email = session['email']
    except:
      print("ERROR: Must be signed in to accept wager")
      abort(500)

    try:
      pubkey = request.form['pubkey']
    except:
      print("ERROR: Must have a pubkey")
      abort(500)

    # Assign user and pubkey to home or away
    if wager.away_id:
      wager.home_id = user_email
      wager.home_pubkey = pubkey
    elif wager.home_id:
      wager.away_id = user_email
      wager.away_pubkey = pubkey
    else:
      print("ERROR: Wager has already been accepted")
      abort(500)

    # Make sure nobody accepts their own wager
    if wager.home_id == wager.away_id:
      print("ERROR: Can't accept your own wager")
      abort(500)

    # Assign user to acceptor
    wager.acceptor_id = user_email

    # Get servers pubkey and assign it
    w = wallet_helper()
    wager.server_pubkey = w.payout_pubkey_str()

    # Create contract and save address + hex
    try:
      script_data = w.create_contract(wager)
    except:
      print("ERROR: Trouble creating multisig redeem script")
      abort(500)

    print(script_data)
    wager.script_address = script_data['script_address']
    wager.script_hex = script_data['script_hex']

    try:
      db.session.commit()
    except:
      print("ERROR: Trouble saving wager to DB")
      abort(500)

    return "Done with ajax request."

  game = mlb.get_mlb_game(wager.game_id)
  return render_template('wager/show.html', wager=wager, game=game, innings=[])

@wagerbp.route('/<path:wager_id>/sign', methods=['GET'])
def sign(wager_id):
  wager = models.MLBWager.query.filter_by(id=wager_id).first()

  return render_template('wager/sign.html', wager=wager)


@wagerbp.route('/<path:wager_id>/stream_events', methods=['GET'])
def stream_events(wager_id):
   wager = models.MLBWager.query.filter_by(id=wager_id).first()
   def generate(wager):
      events = mlb.get_game_events(wager.game_id)
      print("events: {}".format(events))
      res = json.dumps(events['html']['body']['game']['inning'])
      print("res: {}".format(res))

      yield res

   return app.response_class(generate(wager), mimetype='application/json')
