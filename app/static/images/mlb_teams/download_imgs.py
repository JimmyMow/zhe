import urllib.request
import time

teams = ["ARI", "ATL", "BAL", "BOS", "CHC", "CHW", "CIN", "CLE", "COL", "DET", "MIA", "HOU", "KAN", "LAA", "LAD", "MIL", "MIN", "NYM", "NYY", "OAK", "PHI", "PIT", "SD", "SF", "SEA", "STL", "TB", "TEX", "TOR", "WAS"]

for team in teams:
   f = open(team.lower().strip()+'.png','wb')
   f.write(urllib.request.urlopen('http://a.espncdn.com/combiner/i?img=/i/teamlogos/mlb/500/'+team.strip().lower()+'.png&h=150&w=150').read())
   f.close()
   print("done with {}".format(team.lower().strip()))
   time.sleep(3)


