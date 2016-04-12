from app import app
from app.toolbox import mlb

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
def events(game):
   events = game['home']['events'] + game['away']['events']

   def getKey(item):
      return item['inning']

   events_sorted = sorted(events, key=getKey)

   return events_sorted

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
