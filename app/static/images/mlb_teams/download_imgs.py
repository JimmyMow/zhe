import urllib.request
import time

# ESPN
# teams = ["ARI", "ATL", "BAL", "BOS", "CHC", "CHW", "CIN", "CLE", "COL", "DET", "MIA", "HOU", "KAN", "LAA", "LAD", "MIL", "MIN", "NYM", "NYY", "OAK", "PHI", "PIT", "SD", "SF", "SEA", "STL", "TB", "TEX", "TOR", "WAS"]
# MLB
# teams = ["ARI", "ATL", "BAL", "BOS", "CHC", "CWS", "CIN", "CLE", "COL", "DET", "MIA", "HOU", "KC", "ANA", "LAD", "MIL", "MIN", "NYM", "NYY", "OAK", "PHI", "PIT", "SD", "SF", "SEA", "STL", "TB", "TEX", "TOR", "WAS"]

# ESPN
# for team in teams:
#    f = open(team.lower().strip()+'.png','wb')
#    f.write(urllib.request.urlopen('http://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/'+team.strip().lower()+'.png&h=150&w=150').read())
#    f.close()
#    print("done with {}".format(team.lower().strip()))
#    time.sleep(3)

# MLB
# city_dic = {
#    'NYY': 'NYA',
#    'NYM': 'NYN',
#    'CHC': 'CHN',
#    'CWS': 'CHA'
# }
# for team in teams:
#    url = 'http://mlb.mlb.com/mlb/images/team_logos/124x150/' + team.strip().lower() + '@2x.png'
#    f = open("mlb_"+team.lower().strip()+'.png','wb')
#    f.write(urllib.request.urlopen(url).read())
#    f.close()

#    if team in ['NYY', 'NYM', 'CHC', 'CHW']:
#       f = open("mlb_"+city_dic[team].lower().strip()+'.png','wb')
#       f.write(urllib.request.urlopen(url).read())
#       f.close()
#       print("done with {}".format(city_dic[team].strip().lower()))

#    print("done with {}".format(team.lower().strip()))
#    time.sleep(3)

   # TEST
   # try:
   #    a = urllib.request.urlopen(url).read()
   #    print("{} is ok".format(team))
   # except:
   #    print("problem with {}".format(team))

# url = 'http://mlb.mlb.com/mlb/images/team_logos/124x150/sd@2x.png'
# f = open('mlb_sdn.png','wb')
# f.write(urllib.request.urlopen(url).read())
# f.close()
