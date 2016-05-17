from app import app, models, db
from flask import Blueprint, request, session, jsonify

# Create a transaction blueprint
transactionbp = Blueprint('transactionbp', __name__, url_prefix='/transaction')

@transactionbp.route('', methods=['POST'])
def transaction():
   data = request.form

   if request.method == 'POST':
      transaction = models.Transaction(
         user_id=session['email'],
         wager_id=data['wager_id'],
         tx_id=data['tx_id']
      )

      db.session.add(transaction)
      db.session.commit()

      return "success"
