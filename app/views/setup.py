from app import app, models, db
from flask import Flask, render_template, request, Blueprint, session, redirect, url_for, jsonify
from datetime import datetime
from app.toolbox import mlb

# Create a setup blueprint
setupbp = Blueprint('setupbp', __name__, url_prefix='/setup')


@setupbp.route("/bet", methods=['GET', 'POST'])
def setup_bet():
   games = [{'home_team': '4f735188-37c8-473d-ae32-1f7e34ccf892', 'home': {'name': 'Angels', 'market': 'Los Angeles', 'abbr': 'LAA', 'id': '4f735188-37c8-473d-ae32-1f7e34ccf892'}, 'scheduled': '2016-04-06T02:05:00+00:00', 'id': '24740ced-a9dc-46fb-9992-115eb41ac63b', 'away_team': '55714da8-fcaf-4574-8443-59bfb511a524', 'game_number': 1, 'broadcast': {'network': 'CSN+'}, 'status': 'scheduled', 'venue': {'country': 'USA', 'zip': '92806', 'address': '2000 Gene Autry Way', 'name': 'Angel Stadium of Anaheim', 'capacity': 43250, 'id': '60732da9-ad03-4feb-9a36-aee3e98c7a2b', 'city': 'Anaheim', 'surface': 'grass', 'market': 'Los Angeles', 'state': 'CA'}, 'coverage': 'full', 'day_night': 'N', 'away': {'name': 'Cubs', 'market': 'Chicago', 'abbr': 'CHC', 'id': '55714da8-fcaf-4574-8443-59bfb511a524'}}, {'home_team': '03556285-bdbb-4576-a06d-42f71f46ddc5', 'home': {'name': 'Marlins', 'market': 'Miami', 'abbr': 'MIA', 'id': '03556285-bdbb-4576-a06d-42f71f46ddc5'}, 'scheduled': '2016-04-05T23:10:00+00:00', 'id': 'b6f922df-46c6-483c-8d3b-4235a6fc4520', 'away_team': '575c19b7-4052-41c2-9f0a-1c5813d02f99', 'game_number': 1, 'broadcast': {'network': 'MLBN'}, 'status': 'scheduled', 'venue': {'country': 'USA', 'zip': '33125', 'address': '501 Marlins Way', 'name': 'Marlins Park', 'capacity': 36742, 'id': 'd5a66fb3-ff26-4f36-910c-3df5cedb36b3', 'city': 'Miami', 'surface': 'grass', 'market': 'Miami', 'state': 'FL'}, 'coverage': 'full', 'day_night': 'N', 'away': {'name': 'Tigers', 'market': 'Detroit', 'abbr': 'DET', 'id': '575c19b7-4052-41c2-9f0a-1c5813d02f99'}}, {'home_team': 'dcfd5266-00ce-442c-bc09-264cd20cf455', 'home': {'name': 'Brewers', 'market': 'Milwaukee', 'abbr': 'MIL', 'id': 'dcfd5266-00ce-442c-bc09-264cd20cf455'}, 'scheduled': '2016-04-06T00:10:00+00:00', 'id': 'f1229222-d536-4344-b26c-7a97990f7da6', 'away_team': 'a7723160-10b7-4277-a309-d8dd95a8ae65', 'game_number': 1, 'broadcast': {'network': 'FSWI'}, 'status': 'scheduled', 'venue': {'country': 'USA', 'zip': '53214', 'address': 'One Brewers Way', 'name': 'Miller Park', 'capacity': 41900, 'id': '3d13c8a7-283f-482b-ade1-441e25b6465d', 'city': 'Milwaukee', 'surface': 'grass', 'market': 'Milwaukee', 'state': 'WI'}, 'coverage': 'full', 'day_night': 'N', 'away': {'name': 'Giants', 'market': 'San Francisco', 'abbr': 'SF', 'id': 'a7723160-10b7-4277-a309-d8dd95a8ae65'}}, {'home_team': 'd52d5339-cbdd-43f3-9dfa-a42fd588b9a3', 'home': {'name': 'Padres', 'market': 'San Diego', 'abbr': 'SD', 'id': 'd52d5339-cbdd-43f3-9dfa-a42fd588b9a3'}, 'scheduled': '2016-04-06T02:10:00+00:00', 'id': 'dd612e6d-4322-4301-90ef-2c53dd24af96', 'away_team': 'ef64da7f-cfaf-4300-87b0-9313386b977c', 'game_number': 1, 'broadcast': {'network': 'FSSD'}, 'status': 'scheduled', 'venue': {'country': 'USA', 'zip': '92101', 'address': '100 Park Blvd.', 'name': 'PETCO Park', 'capacity': 42302, 'id': '0ab45d79-5475-4308-9f94-74b0c185ee6f', 'city': 'San Diego', 'surface': 'grass', 'market': 'San Diego', 'state': 'CA'}, 'coverage': 'full', 'day_night': 'N', 'away': {'name': 'Dodgers', 'market': 'Los Angeles', 'abbr': 'LAD', 'id': 'ef64da7f-cfaf-4300-87b0-9313386b977c'}}, {'home_team': 'a09ec676-f887-43dc-bbb3-cf4bbaee9a18', 'home': {'name': 'Yankees', 'market': 'New York', 'abbr': 'NYY', 'id': 'a09ec676-f887-43dc-bbb3-cf4bbaee9a18'}, 'scheduled': '2016-04-05T17:05:00+00:00', 'id': '983612c8-997a-4e5a-9b90-6f7a33fed47e', 'away_team': 'eb21dadd-8f10-4095-8bf3-dfb3b779f107', 'game_number': 1, 'broadcast': {'network': 'ESPN '}, 'rescheduled': [{'from': '2016-04-04T17:05:00+00:00', 'reason': 'postponed'}], 'status': 'inprogress', 'venue': {'country': 'USA', 'zip': '10451', 'address': 'One East 161st Street', 'name': 'Yankee Stadium', 'capacity': 49642, 'id': '706e9828-6687-4ac8-a409-3fb972e8bae9', 'city': 'Bronx', 'surface': 'grass', 'market': 'New York', 'state': 'NY'}, 'coverage': 'full', 'day_night': 'D', 'away': {'name': 'Astros', 'market': 'Houston', 'abbr': 'HOU', 'id': 'eb21dadd-8f10-4095-8bf3-dfb3b779f107'}}, {'home_team': '833a51a9-0d84-410f-bd77-da08c3e5e26e', 'home': {'name': 'Royals', 'market': 'Kansas City', 'abbr': 'KC', 'id': '833a51a9-0d84-410f-bd77-da08c3e5e26e'}, 'scheduled': '2016-04-05T20:15:00+00:00', 'id': 'a74496d7-2424-46f6-a029-1f999feb04d4', 'away_team': 'f246a5e5-afdb-479c-9aaa-c68beeda7af6', 'game_number': 1, 'broadcast': {'network': 'FSKC'}, 'status': 'inprogress', 'venue': {'country': 'USA', 'zip': '64129', 'address': 'One Royal Way', 'name': 'Kauffman Stadium', 'capacity': 37903, 'id': '6fca95c9-7f2c-4acb-a9f3-02ef96340d2a', 'city': 'Kansas City', 'surface': 'grass', 'market': 'Kansas City', 'state': 'MO'}, 'coverage': 'full', 'day_night': 'D', 'away': {'name': 'Mets', 'market': 'New York', 'abbr': 'NYM', 'id': 'f246a5e5-afdb-479c-9aaa-c68beeda7af6'}}, {'home_team': '27a59d3b-ff7c-48ea-b016-4798f560f5e1', 'home': {'name': 'Athletics', 'market': 'Oakland', 'abbr': 'OAK', 'id': '27a59d3b-ff7c-48ea-b016-4798f560f5e1'}, 'scheduled': '2016-04-06T02:05:00+00:00', 'id': '9a5d74a2-eb98-4260-8951-6fe654ec27da', 'away_team': '47f490cd-2f58-4ef7-9dfd-2ad6ba6c1ae8', 'game_number': 1, 'broadcast': {'network': 'MLBN'}, 'status': 'scheduled', 'venue': {'country': 'USA', 'zip': '94621', 'address': '7000 Coliseum Way', 'name': 'Oakland Coliseum', 'capacity': 37090, 'id': '48cbd35a-d932-4a75-beab-067bfbacfc26', 'city': 'Oakland', 'surface': 'grass', 'market': 'Oakland', 'state': 'CA'}, 'coverage': 'full', 'day_night': 'N', 'away': {'name': 'White Sox', 'market': 'Chicago', 'abbr': 'CWS', 'id': '47f490cd-2f58-4ef7-9dfd-2ad6ba6c1ae8'}}, {'home_team': 'bdc11650-6f74-49c4-875e-778aeb7632d9', 'home': {'name': 'Rays', 'market': 'Tampa Bay', 'abbr': 'TB', 'id': 'bdc11650-6f74-49c4-875e-778aeb7632d9'}, 'scheduled': '2016-04-05T23:10:00+00:00', 'id': '1ea8e3af-f665-4e95-a1c1-b637d5773a47', 'away_team': '1d678440-b4b1-4954-9b39-70afb3ebbcfa', 'game_number': 1, 'broadcast': {'network': 'Sun Sports'}, 'status': 'scheduled', 'venue': {'country': 'USA', 'zip': '33705', 'address': 'One Tropicana Drive', 'name': 'Tropicana Field', 'capacity': 31042, 'id': '3aaaf4af-0f8c-49c1-8bf1-1780bb5a5f5c', 'city': 'St. Petersburg', 'surface': 'turf', 'market': 'Tampa Bay', 'state': 'FL'}, 'coverage': 'full', 'day_night': 'N', 'away': {'name': 'Blue Jays', 'market': 'Toronto', 'abbr': 'TOR', 'id': '1d678440-b4b1-4954-9b39-70afb3ebbcfa'}}, {'home_team': 'd99f919b-1534-4516-8e8a-9cd106c6d8cd', 'home': {'name': 'Rangers', 'market': 'Texas', 'abbr': 'TEX', 'id': 'd99f919b-1534-4516-8e8a-9cd106c6d8cd'}, 'scheduled': '2016-04-06T00:05:00+00:00', 'id': 'e804db07-6ae2-4e6e-9836-f3e4e87dd999', 'away_team': '43a39081-52b4-4f93-ad29-da7f329ea960', 'game_number': 1, 'broadcast': {'network': 'FSSW'}, 'status': 'scheduled', 'venue': {'country': 'USA', 'zip': '76011', 'address': '1000 Ballpark Way', 'name': 'Globe Life Park in Arlington', 'capacity': 48114, 'id': '3f47c1c6-b059-4fa2-9d85-5d37b7000992', 'city': 'Arlington', 'surface': 'grass', 'market': 'Texas', 'state': 'TX'}, 'coverage': 'full', 'day_night': 'N', 'away': {'name': 'Mariners', 'market': 'Seattle', 'abbr': 'SEA', 'id': '43a39081-52b4-4f93-ad29-da7f329ea960'}}, {'home_team': '25507be1-6a68-4267-bd82-e097d94b359b', 'home': {'name': 'Diamondbacks', 'market': 'Arizona', 'abbr': 'ARI', 'id': '25507be1-6a68-4267-bd82-e097d94b359b'}, 'scheduled': '2016-04-06T01:40:00+00:00', 'id': '968a201d-3aee-4d5e-b118-55c949d9a305', 'away_team': '29dd9a87-5bcc-4774-80c3-7f50d985068b', 'game_number': 1, 'broadcast': {'network': 'FS-A+'}, 'status': 'scheduled', 'venue': {'country': 'USA', 'zip': '85004', 'address': '401 East Jefferson Street', 'name': 'Chase Field', 'capacity': 48633, 'id': 'bf05de0d-7ced-4a19-8e17-2bbd985f8a92', 'city': 'Phoenix', 'surface': 'grass', 'market': 'Arizona', 'state': 'AZ'}, 'coverage': 'full', 'day_night': 'N', 'away': {'name': 'Rockies', 'market': 'Colorado', 'abbr': 'COL', 'id': '29dd9a87-5bcc-4774-80c3-7f50d985068b'}}, {'home_team': '481dfe7e-5dab-46ab-a49f-9dcc2b6e2cfd', 'home': {'name': 'Pirates', 'market': 'Pittsburgh', 'abbr': 'PIT', 'id': '481dfe7e-5dab-46ab-a49f-9dcc2b6e2cfd'}, 'scheduled': '2016-04-05T23:05:00+00:00', 'id': '0d4e3c8a-474d-4d37-9318-5a0be677a020', 'away_team': '44671792-dc02-4fdd-a5ad-f5f17edaa9d7', 'game_number': 1, 'broadcast': {'network': 'FS-M'}, 'status': 'scheduled', 'venue': {'country': 'USA', 'zip': '15212', 'address': '115 Federal Street', 'name': 'PNC Park', 'capacity': 38362, 'id': '61314394-c8b8-411e-b891-ca41285d5362', 'city': 'Pittsburgh', 'surface': 'grass', 'market': 'Pittsburgh', 'state': 'PA'}, 'coverage': 'full', 'day_night': 'N', 'away': {'name': 'Cardinals', 'market': 'St. Louis', 'abbr': 'STL', 'id': '44671792-dc02-4fdd-a5ad-f5f17edaa9d7'}}, {'home_team': '80715d0d-0d2a-450f-a970-1b9a3b18c7e7', 'home': {'name': 'Indians', 'market': 'Cleveland', 'abbr': 'CLE', 'id': '80715d0d-0d2a-450f-a970-1b9a3b18c7e7'}, 'scheduled': '2016-04-05T17:10:00+00:00', 'id': 'bcd65f36-4cb5-4ed5-a13c-410b996e53f7', 'away_team': '93941372-eb4c-4c40-aced-fe3267174393', 'game_number': 1, 'broadcast': {'network': 'SportsTime Ohio'}, 'rescheduled': [{'from': '2016-04-04T20:10:00+00:00', 'reason': 'postponed'}], 'status': 'inprogress', 'venue': {'country': 'USA', 'zip': '44115', 'address': '2401 Ontario Street', 'name': 'Progressive Field', 'capacity': 38000, 'id': '2b0ccd49-4d87-4996-ac4d-27ffc7ee4c16', 'city': 'Cleveland', 'surface': 'grass', 'market': 'Cleveland', 'state': 'OH'}, 'coverage': 'full', 'day_night': 'D', 'away': {'name': 'Red Sox', 'market': 'Boston', 'abbr': 'BOS', 'id': '93941372-eb4c-4c40-aced-fe3267174393'}}]
   if request.method == 'GET':
      return render_template('setup/bet.html', games=games)

   if request.method == 'POST':
      return "here from method post"

@setupbp.route("/friend", methods=['GET', 'POST'])
def setup_friend():
   if 'email' not in session:
      print('User not signed in')
      return abort(500)

   user = models.User.query.filter_by(email=session['email']).first()
   games = mlb.get_todays_games()
   if request.method == 'GET':
      return render_template('setup/friend.html', games=games, user_wallet_seed=user.wallet_seed)

   if request.method == 'POST':
      if 'email' not in session:
        return redirect('/')

      data = request.form

      date_object = datetime.strptime(data['time_date']+'PM', '%Y/%m/%d %I:%M%p')

      mlb_wager = models.MLBWager(
         author_id=session['email'],
         game_id=data['game_id'],
         value=float(data['value']),
         spread=float(data['spread']),
         line=int(data['line']),
         public=False,
         time_date=date_object,
         btc_stamp=float(data['btc_stamp'])
      )

      if data['team_status'] == 'home':
         mlb_wager.home_id = session['email']
         mlb_wager.original_side = 'home'
         mlb_wager.home_pubkey = data['pubkey']
         mlb_wager.home_derive_index = data['derive_index']
      else:
         mlb_wager.away_id = session['email']
         mlb_wager.original_side = 'away'
         mlb_wager.away_pubkey = data['pubkey']
         mlb_wager.away_derive_index = data['derive_index']

      # Insert the user in the database
      db.session.add(mlb_wager)
      db.session.commit()

      data = { 'id': mlb_wager.id }

      return jsonify(data)

