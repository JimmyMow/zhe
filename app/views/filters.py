from app import app
from app.toolbox import mlb
from flask import stream_with_context, request, Response
from dateutil import parser
import time

teams_by_name = {'Cubs': 'Chicago', 'Dodgers': 'Los Angeles', 'Reds': 'Cincinnati', 'Nationals': 'Washington', 'Brewers': 'Milwaukee', 'Diamondbacks': 'Arizona', 'Padres': 'San Diego', 'Braves': 'Atlanta', 'Mets': 'New York', 'Blue Jays': 'Toronto', 'Tigers': 'Detroit', 'Orioles': 'Baltimore', 'Rangers': 'Texas', 'Marlins': 'Miami', 'Rockies': 'Colorado', 'Athletics': 'Oakland', 'Astros': 'Houston', 'Pirates': 'Pittsburgh', 'Cardinals': 'St. Louis', 'Mariners': 'Seattle', 'Indians': 'Cleveland', 'Royals': 'Kansas City', 'Giants': 'San Francisco', 'Red Sox': 'Boston', 'Twins': 'Minnesota', 'Rays': 'Tampa Bay', 'Phillies': 'Philadelphia'}

@app.template_filter('date')
def _jinja2_filter_datetime(date, fmt=None):
   date = date.split("T")
   date_object = datetime.strptime(date[0], '%Y-%m-%d')
   return date_object.strftime('%B %d')

@app.template_filter('oppo')
def oppo(spread):
   oppo_spread = spread * -1
   if oppo_spread > 0:
      oppo_spread = "+"+str(oppo_spread)

   return oppo_spread


@app.template_filter('winnings')
def winnings(wager):

   value = wager.value
   line = wager.line
   if line < 0:
      multiplier = 100 / abs(line)
      payout = value * multiplier
   elif line > 0:
      multiplier = line / 100
      payout = value * multiplier
   else:
      payout = value

   return payout

@app.template_filter('events')
def events(wager):
   # res = mlb.get_game_events(wager.game_id)
   # return res['html']['body']['game']['inning']
   return "dick"

@app.template_filter('player')
def player(player_id):
   player = mlb.get_player(player_id)
   return player

@app.template_filter('city')
def city(name):
   data = name.split(" ")

   if len(data) > 2:
      city = data[0] + " " + data[1]
   else:
      city = data[0]

   return city

@app.template_filter('team_name')
def team_name(name):
   data = name.split(" ")

   if len(data) > 2:
      team_name = data[2]
   else:
      team_name = data[1]

   return team_name

@app.template_filter('city_from_name')
def city_from_name(name):
   city = teams_by_name[name]

   return city

@app.template_filter('pretty_date')
def pretty_date(date_str):

   dt = parser.parse(date_str)
   return dt.strftime("%A, %B %d, %Y")

@app.template_filter('display_pitcher')
def display_pitcher(pitcher_data, key):

   if type(pitcher_data) is list:
      return pitcher_data[0][key]
   elif type(pitcher_data) is dict:
      return pitcher_data[key]
   else:
      return "Error"

@app.template_filter('boxscore_inning')
def boxscore_inning(inning, side):
   try:
      return inning[side]
   except:
      return ""

@app.template_filter('probable_pitcher')
def boxscore_inning(data, side):
   if side == 'away':
      return "{} {}, {} #{}".format(data['away_probable_pitcher']['first'], data['away_probable_pitcher']['last'], data['away_probable_pitcher']['throwinghand'], data['away_probable_pitcher']['number'])
   else:
      return "{} {}, {} #{}".format(data['home_probable_pitcher']['first'], data['home_probable_pitcher']['last'], data['home_probable_pitcher']['throwinghand'], data['home_probable_pitcher']['number'])
