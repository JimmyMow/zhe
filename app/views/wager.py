from flask import Blueprint, render_template, url_for, Response, stream_with_context, request, abort, session, jsonify
from app import app, models, db

from app.toolbox import mlb
from app.toolbox.wallet_helper import wallet_helper

from datetime import datetime
from math import sqrt
import time
import json
import math

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
      derive_index = request.form['derive_index']
    except:
      print("ERROR: Must have a pubkey and derive index")
      abort(500)

    # Assign user and pubkey to home or away
    if wager.away_id:
      wager.home_id = user_email
      wager.home_pubkey = pubkey
      wager.home_derive_index = derive_index
    elif wager.home_id:
      wager.away_id = user_email
      wager.away_pubkey = pubkey
      wager.away_derive_index = derive_index
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

    owe = wager.owe(user_email)
    owe_in_satoshis = w.usd_to_satoshi(owe, wager.btc_stamp)

    data = { 'owe': owe_in_satoshis, 'script_address': wager.script_address }

    return jsonify(data)

  game = mlb.get_mlb_game(wager.game_id)
  expired = math.floor(((wager.time_date - datetime.now()).seconds) / 3600) > 0
  fee_pb = wallet_helper.rec_fee()['fastestFee']
  txs = models.Transaction.query.filter_by(wager_id=wager_id).all()
  return render_template('wager/show.html', wager=wager, game=game, expired=expired, fee_pb=fee_pb, txs=txs, innings=[])

@wagerbp.route('/<path:wager_id>/sign', methods=['GET'])
def sign(wager_id):
  wager = models.MLBWager.query.filter_by(id=wager_id).first()

  owe = wager.owe(session['email'])
  print(owe)

  w = wallet_helper()
  owe_in_satoshis = w.usd_to_satoshi(owe, wager.btc_stamp)
  print(owe_in_satoshis)

  return render_template('wager/sign.html', wager=wager)


@wagerbp.route('/<path:wager_id>/stream_events', methods=['GET'])
def stream_events(wager_id):
   wager = models.MLBWager.query.filter_by(id=wager_id).first()
   def generate(wager):
      events = mlb.get_game_events(wager.game_id)
      # print("events: {}".format(events))
      res = json.dumps(events['html']['body']['game']['inning'])
      # print("res: {}".format(res))

      yield res

   return app.response_class(generate(wager), mimetype='application/json')
