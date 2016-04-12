from flask import Blueprint, render_template, url_for
from app import app, models, db
from app.toolbox import mlb
from datetime import datetime


# Create a wager blueprint
wagerbp = Blueprint('wagerbp', __name__, url_prefix='/wager')

@wagerbp.route('', methods=['GET'])
def all_wagers():
    wagers = models.MLBWager.query.all()
    return render_template('wager/all.html', wagers=wagers)

@wagerbp.route('/<path:wager_id>', methods=['GET'])
def wager(wager_id):
    wager = models.MLBWager.query.filter_by(id=wager_id).first()
    game = mlb.get_game(wager.game_id)
    o_game = mlb.get_mlb_game(wager.game_id)
    return render_template('wager/show.html', wager=wager, game=game, o_game=o_game)
