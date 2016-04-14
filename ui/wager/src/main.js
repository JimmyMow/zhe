var m = require('mithril');

var ge = document.getElementById('game_events');

var xmlhttp = new XMLHttpRequest(),
method = "GET",
url = "http://15970801.ngrok.io/wager/cd148f0d/stream_events";

xmlhttp.open(method, url, true);
xmlhttp.onreadystatechange = function () {
   // ge.innerHTML = xmlhttp.responseText;
}
xmlhttp.send();
var timer;
timer = setInterval(function() {
   // stop checking once the response has ended
   if (xmlhttp.readyState == XMLHttpRequest.DONE) {
      buildEvents(xmlhttp.responseText);
      clearInterval(timer);
   }
}, 1000);

var html = m('div.events', [

]);

function buildEvents(data) {
   var innings = JSON.parse(data);
   var html = m('div', {
      class: ['events', 'cf'].join(' ')
   }, innings.map(function(inning) {
      try {
         var away = inning.top.atbat.map(function(atbat) {
            if ( atbat['@score'] ) {
               return m('div', { class: ['score-conatiner', 'cf'].join(' ') },
               m('div', { class: ['score', 'away'].join(' ') },
                  m('div', {class: 'details'},
                     m('p', { class: 'description' }, atbat['@des'])
                  ),
                  m('img', {src: 'http://mlb.mlb.com/images/players/mugshot/ph_' + atbat['@batter'] + '.jpg'})
               ));
            }
         });
      }
      catch(err) {
         var away = {};
      }

      try {
         var home = inning.bottom.atbat.map(function(atbat) {
            if ( atbat['@score'] ) {
               return m('div', { class: ['score-conatiner', 'cf'].join(' ') },
               m('div', { class: ['score', 'home'].join(' ') },
                  m('div', {class: 'details'},
                     m('p', { class: 'description' }, atbat['@des'])
                  ),
                  m('img', {src: 'http://mlb.mlb.com/images/players/mugshot/ph_' + atbat['@batter'] + '.jpg'})
               ));
            }
         });
      }
      catch(err) {
         var home = {};
      }

      return [away, home];
   }));

   console.log(html);

   m.render(ge, html);
}

console.log("yo from wager_show");
