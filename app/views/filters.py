from app import app

@app.template_filter('date')
def _jinja2_filter_datetime(date, fmt=None):
   date = date.split("T")
   date_object = datetime.strptime(date[0], '%Y-%m-%d')
   return date_object.strftime('%B %d')

@app.template_filter('oppo')
def _jinja2_filter_datetime(spread):
   oppo_spread = spread * -1
   if oppo_spread > 0:
      oppo_spread = "+"+str(oppo_spread)

   return oppo_spread


@app.template_filter('winnings')
def _jinja2_filter_datetime(wager):

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
def _jinja2_filter_datetime(game):
   events = game['home']['events'] + game['away']['events']

   def getKey(item):
      return item['inning']

   events_sorted = sorted(events, key=getKey)

   return events_sorted

