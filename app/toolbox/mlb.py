from app import app
from bs4 import BeautifulSoup
import requests
import datetime
import json
import xmltodict

def get_todays_games():
   now = datetime.datetime.now()

   url = "http://gd2.mlb.com/components/game/mlb/year_"+ str(now.year) +"/month_"+ now.strftime('%m') +"/day_"+ str(now.day) +"/epg.xml"
   r = requests.get(url)
   if r.status_code == 200:
      soup = BeautifulSoup(r.text, "lxml")
   else:
      r.raise_for_status()

   games = soup.find_all('game')
   games_arr = []
   for game in games:
      obj = {}
      obj['id'] = game['id']
      obj['home_team_name'] = game['home_team_name']
      obj['home_team_id'] = game['home_team_id']
      obj['away_team_name'] = game['away_team_name']
      obj['away_team_id'] = game['away_team_id']
      obj['away_team_id'] = game['away_team_id']
      obj['gameday'] = game['gameday']
      games_arr.append(obj)

   return games_arr


def get_game(game_id):
   # url = "https://api.sportradar.us/mlb-t5/games/" + game_id + "/boxscore.json?api_key=" + app.config["SPORTRADAR_MLB_KEY"]
   # r = requests.get(url)
   # data = r.json()

   data = {'pitching': {'win': {'preferred_name': 'Jon', 'last_name': 'Lester', 'status': 'A', 'position': 'P', 'jersey_number': '34', 'hold': 0, 'blown_save': 0, 'first_name': 'Jonathan', 'win': 1, 'save': 0, 'id': '46734ad0-e55b-4e2f-8a0d-72387470fcdf', 'primary_position': 'SP', 'loss': 0}, 'loss': {'preferred_name': 'Andrew', 'last_name': 'Heaney', 'status': 'A', 'position': 'P', 'jersey_number': '28', 'hold': 0, 'blown_save': 0, 'first_name': 'Andrew', 'win': 0, 'save': 0, 'id': 'ade46bf9-fcaa-4185-8fc9-79af6d2ec81b', 'primary_position': 'SP', 'loss': 1}}, 'attendance': 37042, 'home_team': '4f735188-37c8-473d-ae32-1f7e34ccf892', 'status': 'closed', 'broadcast': {'network': 'CSN+'}, 'away_team': '55714da8-fcaf-4574-8443-59bfb511a524', 'home': {'hits': 4, 'abbr': 'LAA', 'name': 'Angels', 'events': [{'type': 'pitch', 'runners': [{'preferred_name': 'Yunel', 'first_name': 'Yunel', 'last_name': 'Escobar', 'starting_base': 2, 'id': '9ca64cb3-b29b-4cb4-a048-a5919dcb44a3', 'jersey_number': '6'}], 'pitcher_id': '46734ad0-e55b-4e2f-8a0d-72387470fcdf', 'inning': 6, 'inning_half': 'B', 'hitter_outcome': 'aS', 'id': '82be581d-a0d9-4162-972e-e6ac044765ea', 'hitter_id': '3ee81377-4e48-4d45-9e32-fb2867c63e7d'}], 'probable_pitcher': {'preferred_name': 'Andrew', 'era': 0.0, 'win': 0, 'first_name': 'Andrew', 'last_name': 'Heaney', 'id': 'ade46bf9-fcaa-4185-8fc9-79af6d2ec81b', 'jersey_number': '28', 'loss': 0}, 'id': '4f735188-37c8-473d-ae32-1f7e34ccf892', 'runs': 1, 'errors': 0, 'starting_pitcher': {'preferred_name': 'Andrew', 'era': 0.0, 'win': 0, 'first_name': 'Andrew', 'last_name': 'Heaney', 'id': 'ade46bf9-fcaa-4185-8fc9-79af6d2ec81b', 'jersey_number': '28', 'loss': 0}, 'scoring': [{'type': 'inning', 'sequence': 1, 'number': 1, 'runs': 0}, {'type': 'inning', 'sequence': 2, 'number': 2, 'runs': 0}, {'type': 'inning', 'sequence': 3, 'number': 3, 'runs': 0}, {'type': 'inning', 'sequence': 4, 'number': 4, 'runs': 0}, {'type': 'inning', 'sequence': 5, 'number': 5, 'runs': 0}, {'type': 'inning', 'sequence': 6, 'number': 6, 'runs': 1}, {'type': 'inning', 'sequence': 7, 'number': 7, 'runs': 0}, {'type': 'inning', 'sequence': 8, 'number': 8, 'runs': 0}, {'type': 'inning', 'sequence': 9, 'number': 9, 'runs': 0}], 'market': 'Los Angeles'}, 'scheduled': '2016-04-06T02:05:00+00:00', 'coverage': 'full', 'final': {'inning': 9, 'inning_half': 'B'}, 'venue': {'city': 'Anaheim', 'address': '2000 Gene Autry Way', 'name': 'Angel Stadium of Anaheim', 'zip': '92806', 'id': '60732da9-ad03-4feb-9a36-aee3e98c7a2b', 'surface': 'grass', 'capacity': 43250, 'state': 'CA', 'country': 'USA', 'market': 'Los Angeles'}, 'id': '24740ced-a9dc-46fb-9992-115eb41ac63b', 'day_night': 'N', 'game_number': 1, 'away': {'hits': 9, 'abbr': 'CHC', 'name': 'Cubs', 'events': [{'type': 'pitch', 'runners': [{'preferred_name': 'Matt', 'first_name': 'Matthew', 'last_name': 'Szczur', 'starting_base': 0, 'id': 'ea8fad1f-1c47-4f61-b7c7-9c725f02d9a2', 'jersey_number': '20'}], 'pitcher_id': 'ade46bf9-fcaa-4185-8fc9-79af6d2ec81b', 'inning': 3, 'inning_half': 'T', 'hitter_outcome': 'aHR', 'id': '7a3f086f-fd00-46f1-a9ad-45d6b686e3d5', 'hitter_id': 'ea8fad1f-1c47-4f61-b7c7-9c725f02d9a2'}, {'type': 'pitch', 'runners': [{'preferred_name': 'David', 'first_name': 'David', 'last_name': 'Ross', 'starting_base': 3, 'id': '9a3adad1-958b-4378-8dad-be632cf20e6b', 'jersey_number': '3'}], 'pitcher_id': 'ade46bf9-fcaa-4185-8fc9-79af6d2ec81b', 'inning': 3, 'inning_half': 'T', 'hitter_outcome': 'oFC', 'id': '258a9868-bee2-49b6-afe3-756f036faa61', 'hitter_id': '8e42fd09-b9d0-4566-b960-e107f580de46'}, {'type': 'pitch', 'runners': [{'preferred_name': 'Anthony', 'first_name': 'Anthony', 'last_name': 'Rizzo', 'starting_base': 0, 'id': '75cb4b6c-a087-4b77-90e3-7473284fa8ad', 'jersey_number': '44'}, {'preferred_name': 'Jason', 'first_name': 'Jason', 'last_name': 'Heyward', 'starting_base': 2, 'id': '8e42fd09-b9d0-4566-b960-e107f580de46', 'jersey_number': '22'}], 'pitcher_id': 'ade46bf9-fcaa-4185-8fc9-79af6d2ec81b', 'inning': 3, 'inning_half': 'T', 'hitter_outcome': 'aHR', 'id': '63141a97-bc9a-4de0-a07b-6ddcaf0f914c', 'hitter_id': '75cb4b6c-a087-4b77-90e3-7473284fa8ad'}, {'type': 'pitch', 'runners': [{'preferred_name': 'Dexter', 'first_name': 'William', 'last_name': 'Fowler', 'starting_base': 0, 'id': 'a91b5de2-7809-4c9c-b67a-409835c5f17e', 'jersey_number': '24'}, {'preferred_name': 'Matt', 'first_name': 'Matthew', 'last_name': 'Szczur', 'starting_base': 1, 'id': 'ea8fad1f-1c47-4f61-b7c7-9c725f02d9a2', 'jersey_number': '20'}], 'pitcher_id': 'ba2e1701-825c-43a3-9b7f-604b2859337f', 'inning': 7, 'inning_half': 'T', 'hitter_outcome': 'aHR', 'id': 'c6356bce-5b8b-403c-9935-2759b5f4da24', 'hitter_id': 'a91b5de2-7809-4c9c-b67a-409835c5f17e'}], 'probable_pitcher': {'preferred_name': 'Jon', 'era': 0.0, 'win': 0, 'first_name': 'Jonathan', 'last_name': 'Lester', 'id': '46734ad0-e55b-4e2f-8a0d-72387470fcdf', 'jersey_number': '34', 'loss': 0}, 'id': '55714da8-fcaf-4574-8443-59bfb511a524', 'runs': 6, 'errors': 1, 'starting_pitcher': {'preferred_name': 'Jon', 'era': 0.0, 'win': 0, 'first_name': 'Jonathan', 'last_name': 'Lester', 'id': '46734ad0-e55b-4e2f-8a0d-72387470fcdf', 'jersey_number': '34', 'loss': 0}, 'scoring': [{'type': 'inning', 'sequence': 1, 'number': 1, 'runs': 0}, {'type': 'inning', 'sequence': 2, 'number': 2, 'runs': 0}, {'type': 'inning', 'sequence': 3, 'number': 3, 'runs': 4}, {'type': 'inning', 'sequence': 4, 'number': 4, 'runs': 0}, {'type': 'inning', 'sequence': 5, 'number': 5, 'runs': 0}, {'type': 'inning', 'sequence': 6, 'number': 6, 'runs': 0}, {'type': 'inning', 'sequence': 7, 'number': 7, 'runs': 2}, {'type': 'inning', 'sequence': 8, 'number': 8, 'runs': 0}, {'type': 'inning', 'sequence': 9, 'number': 9, 'runs': 0}], 'market': 'Chicago'}}

   return data

def get_player(player_id):
   url = "http://api.sportradar.us/mlb-t5/players/" + player_id + "/profile.json?api_key=" + app.config["SPORTRADAR_MLB_KEY"]
   r = requests.get(url)
   data = r.json()

   # data = {'pitching': {'win': {'preferred_name': 'Jon', 'last_name': 'Lester', 'status': 'A', 'position': 'P', 'jersey_number': '34', 'hold': 0, 'blown_save': 0, 'first_name': 'Jonathan', 'win': 1, 'save': 0, 'id': '46734ad0-e55b-4e2f-8a0d-72387470fcdf', 'primary_position': 'SP', 'loss': 0}, 'loss': {'preferred_name': 'Andrew', 'last_name': 'Heaney', 'status': 'A', 'position': 'P', 'jersey_number': '28', 'hold': 0, 'blown_save': 0, 'first_name': 'Andrew', 'win': 0, 'save': 0, 'id': 'ade46bf9-fcaa-4185-8fc9-79af6d2ec81b', 'primary_position': 'SP', 'loss': 1}}, 'attendance': 37042, 'home_team': '4f735188-37c8-473d-ae32-1f7e34ccf892', 'status': 'closed', 'broadcast': {'network': 'CSN+'}, 'away_team': '55714da8-fcaf-4574-8443-59bfb511a524', 'home': {'hits': 4, 'abbr': 'LAA', 'name': 'Angels', 'events': [{'type': 'pitch', 'runners': [{'preferred_name': 'Yunel', 'first_name': 'Yunel', 'last_name': 'Escobar', 'starting_base': 2, 'id': '9ca64cb3-b29b-4cb4-a048-a5919dcb44a3', 'jersey_number': '6'}], 'pitcher_id': '46734ad0-e55b-4e2f-8a0d-72387470fcdf', 'inning': 6, 'inning_half': 'B', 'hitter_outcome': 'aS', 'id': '82be581d-a0d9-4162-972e-e6ac044765ea', 'hitter_id': '3ee81377-4e48-4d45-9e32-fb2867c63e7d'}], 'probable_pitcher': {'preferred_name': 'Andrew', 'era': 0.0, 'win': 0, 'first_name': 'Andrew', 'last_name': 'Heaney', 'id': 'ade46bf9-fcaa-4185-8fc9-79af6d2ec81b', 'jersey_number': '28', 'loss': 0}, 'id': '4f735188-37c8-473d-ae32-1f7e34ccf892', 'runs': 1, 'errors': 0, 'starting_pitcher': {'preferred_name': 'Andrew', 'era': 0.0, 'win': 0, 'first_name': 'Andrew', 'last_name': 'Heaney', 'id': 'ade46bf9-fcaa-4185-8fc9-79af6d2ec81b', 'jersey_number': '28', 'loss': 0}, 'scoring': [{'type': 'inning', 'sequence': 1, 'number': 1, 'runs': 0}, {'type': 'inning', 'sequence': 2, 'number': 2, 'runs': 0}, {'type': 'inning', 'sequence': 3, 'number': 3, 'runs': 0}, {'type': 'inning', 'sequence': 4, 'number': 4, 'runs': 0}, {'type': 'inning', 'sequence': 5, 'number': 5, 'runs': 0}, {'type': 'inning', 'sequence': 6, 'number': 6, 'runs': 1}, {'type': 'inning', 'sequence': 7, 'number': 7, 'runs': 0}, {'type': 'inning', 'sequence': 8, 'number': 8, 'runs': 0}, {'type': 'inning', 'sequence': 9, 'number': 9, 'runs': 0}], 'market': 'Los Angeles'}, 'scheduled': '2016-04-06T02:05:00+00:00', 'coverage': 'full', 'final': {'inning': 9, 'inning_half': 'B'}, 'venue': {'city': 'Anaheim', 'address': '2000 Gene Autry Way', 'name': 'Angel Stadium of Anaheim', 'zip': '92806', 'id': '60732da9-ad03-4feb-9a36-aee3e98c7a2b', 'surface': 'grass', 'capacity': 43250, 'state': 'CA', 'country': 'USA', 'market': 'Los Angeles'}, 'id': '24740ced-a9dc-46fb-9992-115eb41ac63b', 'day_night': 'N', 'game_number': 1, 'away': {'hits': 9, 'abbr': 'CHC', 'name': 'Cubs', 'events': [{'type': 'pitch', 'runners': [{'preferred_name': 'Matt', 'first_name': 'Matthew', 'last_name': 'Szczur', 'starting_base': 0, 'id': 'ea8fad1f-1c47-4f61-b7c7-9c725f02d9a2', 'jersey_number': '20'}], 'pitcher_id': 'ade46bf9-fcaa-4185-8fc9-79af6d2ec81b', 'inning': 3, 'inning_half': 'T', 'hitter_outcome': 'aHR', 'id': '7a3f086f-fd00-46f1-a9ad-45d6b686e3d5', 'hitter_id': 'ea8fad1f-1c47-4f61-b7c7-9c725f02d9a2'}, {'type': 'pitch', 'runners': [{'preferred_name': 'David', 'first_name': 'David', 'last_name': 'Ross', 'starting_base': 3, 'id': '9a3adad1-958b-4378-8dad-be632cf20e6b', 'jersey_number': '3'}], 'pitcher_id': 'ade46bf9-fcaa-4185-8fc9-79af6d2ec81b', 'inning': 3, 'inning_half': 'T', 'hitter_outcome': 'oFC', 'id': '258a9868-bee2-49b6-afe3-756f036faa61', 'hitter_id': '8e42fd09-b9d0-4566-b960-e107f580de46'}, {'type': 'pitch', 'runners': [{'preferred_name': 'Anthony', 'first_name': 'Anthony', 'last_name': 'Rizzo', 'starting_base': 0, 'id': '75cb4b6c-a087-4b77-90e3-7473284fa8ad', 'jersey_number': '44'}, {'preferred_name': 'Jason', 'first_name': 'Jason', 'last_name': 'Heyward', 'starting_base': 2, 'id': '8e42fd09-b9d0-4566-b960-e107f580de46', 'jersey_number': '22'}], 'pitcher_id': 'ade46bf9-fcaa-4185-8fc9-79af6d2ec81b', 'inning': 3, 'inning_half': 'T', 'hitter_outcome': 'aHR', 'id': '63141a97-bc9a-4de0-a07b-6ddcaf0f914c', 'hitter_id': '75cb4b6c-a087-4b77-90e3-7473284fa8ad'}, {'type': 'pitch', 'runners': [{'preferred_name': 'Dexter', 'first_name': 'William', 'last_name': 'Fowler', 'starting_base': 0, 'id': 'a91b5de2-7809-4c9c-b67a-409835c5f17e', 'jersey_number': '24'}, {'preferred_name': 'Matt', 'first_name': 'Matthew', 'last_name': 'Szczur', 'starting_base': 1, 'id': 'ea8fad1f-1c47-4f61-b7c7-9c725f02d9a2', 'jersey_number': '20'}], 'pitcher_id': 'ba2e1701-825c-43a3-9b7f-604b2859337f', 'inning': 7, 'inning_half': 'T', 'hitter_outcome': 'aHR', 'id': 'c6356bce-5b8b-403c-9935-2759b5f4da24', 'hitter_id': 'a91b5de2-7809-4c9c-b67a-409835c5f17e'}], 'probable_pitcher': {'preferred_name': 'Jon', 'era': 0.0, 'win': 0, 'first_name': 'Jonathan', 'last_name': 'Lester', 'id': '46734ad0-e55b-4e2f-8a0d-72387470fcdf', 'jersey_number': '34', 'loss': 0}, 'id': '55714da8-fcaf-4574-8443-59bfb511a524', 'runs': 6, 'errors': 1, 'starting_pitcher': {'preferred_name': 'Jon', 'era': 0.0, 'win': 0, 'first_name': 'Jonathan', 'last_name': 'Lester', 'id': '46734ad0-e55b-4e2f-8a0d-72387470fcdf', 'jersey_number': '34', 'loss': 0}, 'scoring': [{'type': 'inning', 'sequence': 1, 'number': 1, 'runs': 0}, {'type': 'inning', 'sequence': 2, 'number': 2, 'runs': 0}, {'type': 'inning', 'sequence': 3, 'number': 3, 'runs': 4}, {'type': 'inning', 'sequence': 4, 'number': 4, 'runs': 0}, {'type': 'inning', 'sequence': 5, 'number': 5, 'runs': 0}, {'type': 'inning', 'sequence': 6, 'number': 6, 'runs': 0}, {'type': 'inning', 'sequence': 7, 'number': 7, 'runs': 2}, {'type': 'inning', 'sequence': 8, 'number': 8, 'runs': 0}, {'type': 'inning', 'sequence': 9, 'number': 9, 'runs': 0}], 'market': 'Chicago'}}

   return data

def get_mlb_game(game_id):
   game_data = game_id.split("/")
   year = game_data[0]
   month = game_data[1]
   day = game_data[2]

   boxscore_url = "http://gd2.mlb.com/components/game/mlb/year_" + year + "/month_" + month + "/day_" + day + "/gid_" + game_id.replace('/', '_').replace('-', '_') + "/boxscore.json"
   scoreline_url = "http://gd2.mlb.com/components/game/mlb/year_" + year + "/month_" + month + "/day_" + day + "/gid_" + game_id.replace('/', '_').replace('-', '_') + "/linescore.json"

   try:
      r = requests.get(boxscore_url)
      data = r.json()
      return data
   except:
      r = requests.get(scoreline_url)
      data = r.json()
      return data

def get_scoring_plays(game_id):
   game_data = game_id.split("/")
   year = game_data[0]
   month = game_data[1]
   day = game_data[2]

   url = "http://gd2.mlb.com/components/game/mlb/year_"+year+"/month_"+month+"/day_"+day+"/gid_"+game_id.replace('/', '_').replace('-', '_')+"/atv_runScoringPlays.xml"
   r = requests.get(url)
   if r.status_code == 200:
      soup = BeautifulSoup(r.text, "lxml")
      result = json.dumps(xmltodict.parse(str(soup)))
   else:
      r.raise_for_status()
      return

   return json.loads(result)

def get_game_events(game_id):
   game_data = game_id.split("/")
   year = game_data[0]
   month = game_data[1]
   day = game_data[2]

   url = "http://gd2.mlb.com/components/game/mlb/year_"+year+"/month_"+month+"/day_"+day+"/gid_"+game_id.replace('/', '_').replace('-', '_')+"/game_events.xml"
   r = requests.get(url)
   if r.status_code == 200:
      soup = BeautifulSoup(r.text, "lxml")
      result = json.dumps(xmltodict.parse(str(soup)))
   else:
      r.raise_for_status()

   return json.loads(result)
