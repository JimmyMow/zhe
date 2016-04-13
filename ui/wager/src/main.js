var ctrl = require('./ctrl');
var xhr = require('./xhr');

// xhr.game_events().then(function(events) {
//    console.log("events: ", events)
// });

$.ajax({
    type: "GET",
    dataType: 'json',
    url: "http://gd2.mlb.com/components/game/mlb/year_2016/month_04/day_12/gid_2016_04_11_pitmlb_detmlb_1/game_events.json",
    crossDomain : true,
    xhrFields: {
        withCredentials: true
    }
})
    .done(function( data ) {
        console.log("done");
    })
    .fail( function(xhr, textStatus, errorThrown) {
        console.log(xhr.responseText);
        console.log(textStatus);
    });

console.log("yo from wager_show");
