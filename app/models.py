from app import db, bcrypt
from app.toolbox import json_helper
from sqlalchemy.ext.hybrid import hybrid_property
from flask.ext.login import UserMixin
from sqlalchemy import *
from sqlalchemy import event
import uuid

class User(db.Model, UserMixin):

    ''' Zero House Edge user. '''

    __tablename__ = 'users'
    email = db.Column(db.String, primary_key=True)
    payout_address = db.Column(db.String)
    wallet_seed = db.Column(db.String)
    _password = db.Column(db.String)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)

    def check_password(self, plaintext):
        return bcrypt.check_password_hash(self.password, plaintext)

    def get_id(self):
        return self.email

class MLBWager(db.Model):

    ''' Zero House Edge MLB Wager on a game's final score. '''

    __tablename__ = 'mlbwagers'
    id = db.Column(db.String, primary_key=True)

    author_id = db.Column(db.String)
    acceptor_id = db.Column(db.String)

    home_id = db.Column(db.String)
    away_id = db.Column(db.String)


    home_pubkey = db.Column(db.String)
    away_pubkey = db.Column(db.String)
    server_pubkey = db.Column(db.String)

    game_id = db.Column(db.String)
    original_side = db.Column(db.String)
    spread = db.Column(db.Integer)
    line = db.Column(db.Float)
    value = db.Column(db.Integer)

    public = db.Column(db.Boolean)

    script_address = db.Column(db.String)
    script_hex = db.Column(db.String)

    time_date = db.Column(db.DateTime)

    btc_stamp = db.Column(db.Float)

    away_derive_index = db.Column(db.Integer)
    home_derive_index = db.Column(db.Integer)

    @property
    def json(self):
        return json_helper.to_json(self, self.__class__)

    def owe(self, user_email):
        if self.home_id == user_email:
            x = "home"
        elif self.away_id == user_email:
            x = "away"
        else:
            return None

        if self.original_side == x:
            payout = self.value
        else:
            if(self.line < 0):
                multiplier = 100 / abs(self.line)
                payout = self.value * multiplier
            elif self.line > 0:
                multiplier = self.line / 100
                payout = self.value * multiplier
            else:
                payout = self.value

        return payout

    def winner(self, data):
        h_score = data['home_team_runs']
        a_score = data['away_team_runs']
        if self.original_side == 'away':
            home_total = int(h_score)
            away_total = int(a_score) + (int(self.spread))
        else:
            away_total = int(a_score)
            home_total = int(h_score) + (int(self.spread))

        return self.home_pubkey if home_total > away_total else self.away_pubkey

    def away_user(self):
        away_user = db.session.query(User).filter_by(email=self.away_id).first()
        return away_user

    def home_user(self):
        home_user = db.session.query(User).filter_by(email=self.home_id).first()
        return home_user

    def funded(self):
        txs = db.session.query(Transaction).filter_by(wager_id=self.id, output=False).all()
        return txs

class Transaction(db.Model):
    ''' A transaction to the multisig redeem script. '''

    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    wager_id = db.Column(db.String)
    user_id = db.Column(db.String)
    tx_id = db.Column(db.String)
    hex = db.Column(db.String)
    output = db.Column(db.Boolean, default=False)

    def blockexplorer(self):
        return "https://blockexplorer.com/tx/" + self.tx_id

# Generate random string for ID of the MLB Wager
def after_insert_listener(mapper, connection, target):
    target.id = str(uuid.uuid4())[:8]

event.listen(MLBWager, 'before_insert', after_insert_listener)
