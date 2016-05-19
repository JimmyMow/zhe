from flask import Blueprint, render_template, url_for, Response, stream_with_context, request, abort, session, jsonify
from app import app, models, db

from app.toolbox import mlb
from app.toolbox.wallet_helper import wallet_helper

from datetime import datetime
from math import sqrt
import time
import json
import math

import two1.bitcoin as bitcoin

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
  away_tx = models.Transaction.query.filter_by(wager_id=wager_id, user_id=wager.away_id).first()
  home_tx = models.Transaction.query.filter_by(wager_id=wager_id, user_id=wager.home_id).first()
  return render_template('wager/show.html', wager=wager, game=game, expired=expired, fee_pb=fee_pb, home_tx=home_tx, away_tx=away_tx, innings=[])

@wagerbp.route('/<path:wager_id>/sign', methods=['GET'])
def sign(wager_id):
  if request.method == "POST":
    print('here at sign post')


  wager = models.MLBWager.query.filter_by(id=wager_id).first()
  game = mlb.get_mlb_game(wager.game_id)
  txs = models.Transaction.query.filter_by(wager_id=wager_id)
  winner = wager.winner(game['data']['boxscore']['linescore'])

  output_transaction = models.Transaction.query.filter_by(output=True, wager_id=wager_id).first()
  if not output_transaction:

    # Get data on user input txs
    redeem_script = wallet_helper.create_redeem_script(wager)
    input_txs = []
    output_value = 0
    for tx in txs:
      tx_obj = {}
      tx_hex = wallet_helper.get_tx_hex(tx.tx_id)

      txn = wallet_helper.load_tx(tx_hex)
      tx_index = txn.output_index_for_address(redeem_script.hash160())
      tx_obj['tx'] = txn
      tx_obj['tx_index'] = tx_index
      tx_obj['val'] = txn.outputs[int(tx_index)].value
      output_value = output_value + txn.outputs[int(tx_index)].value
      input_txs.append(tx_obj)

    # tx inputs
    script_sig = bitcoin.Script()
    inputs = []
    for in_tx in input_txs:
      deposit_tx = wallet_helper.load_wallet_tx(in_tx['tx'].to_hex())
      inputs.append(bitcoin.TransactionInput(deposit_tx.hash, int(in_tx['tx_index']), script_sig, 0xffffffff))


    fee = 5000
    output_price = output_value - fee
    outputs = [bitcoin.TransactionOutput(int(output_price), bitcoin.Script.build_p2pkh(bitcoin.crypto.PublicKey.from_bytes(winner).hash160()))]

    payment_tx = bitcoin.Transaction(bitcoin.Transaction.DEFAULT_TRANSACTION_VERSION, inputs, outputs, 0x0)
    server_priv_key = wallet_helper.get_priv_for_pub(wager.server_pubkey)

    for i, inp in enumerate(payment_tx.inputs):
      payment_tx.sign_input(i, bitcoin.Transaction.SIG_HASH_ALL, server_priv_key, redeem_script)

    output_transaction = models.Transaction(
      wager_id=wager.id,
      hex=payment_tx.to_hex(),
      output=True
    )

    db.session.add(output_transaction)
    db.session.commit()

  return render_template('wager/_sign.html', wager=wager, txs=txs, winner=winner, output_transaction=output_transaction)


@wagerbp.route('/<path:wager_id>/stream_events', methods=['GET'])
def stream_events(wager_id):
   wager = models.MLBWager.query.filter_by(id=wager_id).first()
   def generate(wager):
      events = mlb.get_game_events(wager.game_id)
      res = json.dumps(events['html']['body']['game']['inning'])

      yield res

   return app.response_class(generate(wager), mimetype='application/json')

@wagerbp.route('/<path:wager_id>/email_bet_accepted', methods=['GET'])
def email_bet_accepted(wager_id):
   print("HERERERERERE")
   wager = models.MLBWager.query.filter_by(id=wager_id).first()
   author = wager.author_id
   acceptor = wager.acceptor_id
   html = render_template('email/bet_accepted.html', author_email=author, acceptor_email=acceptor)
   email.send_email([author_email], "Your bet has been accepted on Zero House Edge", html)
   return "success"
