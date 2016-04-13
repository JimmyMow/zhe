var m = require('mithril');

var xhrConfig = function(xhr) {
  xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  // xhr.setRequestHeader('Accept', 'application/vnd.lichess.v1+json');
}

module.exports = {
  game_events: function() {
    return m.request({
      method: 'GET',
      url: "http://gd2.mlb.com/components/game/mlb/year_2016/month_04/day_12/gid_2016_04_11_pitmlb_detmlb_1/game_events.json",
      config: xhrConfig
    });
  }
};
