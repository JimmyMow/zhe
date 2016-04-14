var m = require('mithril');
// var util = require('chessground').util;
function spinner() {
  return m('div.spinner',
    m('svg', {
      viewBox: '0 0 40 40'
    }, m('circle', {
      cx: 20,
      cy: 20,
      r: 18,
      fill: 'none'
    })));
}

function px(v) {
  return v + 'px';
}

function ratingLog(a) {
  return Math.log(a / 150 + 1);
}


function ratingY(e) {
  var rating = Math.max(1000, Math.min(2200, e || 1500));
  var ratio;
  var mid = 2/5;
  if (rating == 1500) {
    ratio = mid;
  } else if (rating > 1500) {
    ratio = mid + (ratingLog(rating - 1500) / ratingLog(1300)) * 2 * mid;
  } else {
    ratio = mid - (ratingLog(1500 - rating) / ratingLog(500)) * mid;
  }
  return Math.round(ratio * 489);
}

function clockX(dur) {
  function durLog(a) {
    return Math.log((a - 30) / 200 + 1);
  }
  var max = 2000;
  return Math.round(durLog(Math.min(max, dur || max)) / durLog(max) * 489);
}

function renderXAxis() {
  return [1, 2, 3, 5, 7, 10, 15, 20, 30].map(function(v) {
    var l = clockX(v * 60);
    return [
      m('span', {
        class: 'x label',
        style: {
          left: px(l)
        }
      }, v),
      m('div', {
        class: 'grid vert',
        style: {
          width: px(l + 7)
        }
      })
    ];
  });
}


function renderYAxis() {
  return [1000, 1200, 1400, 1500, 1600, 1800, 2000].map(function(v) {
    var b = ratingY(v);
    return [
      m('span', {
        class: 'y label',
        style: {
          bottom: px(b + 5)
        }
      }, v),
      m('div', {
        class: 'grid horiz',
        style: {
          height: px(b + 4)
        }
      })
    ];
  });
}

function renderPlot(hook) {
  console.log(hook)
  var bottom = Math.max(0, ratingY(hook.rating) - 7);
  var left = Math.max(0, clockX(hook.t) - 4);
  var klass = [
    'plot new',
    hook.ra ? 'rated' : 'casual',
    hook.action === 'cancel' ? 'cancel' : '',
    hoom.team
  ].join(' ');
  var span = m('span', {
    id: hook.id,
    key: hook.id,
    class: klass,
    style: {
      bottom: px(bottom),
      left: px(left)
    }
  });
  console.log(span);
  return span;
}
var ctrl = {};
var hooks = [{rating: 2012, t: 60, id: 'dsbhjds', ra: true, action: '', team: 'cubs'}, {rating: 1800, t: 320, id: 'fddffdfd', ra: true, action: '', team: 'angels'}];
var html = m('div.hooks_chart', [
   m('div.canvas', {
      onclick: function(e) {
         console.log(e);
      }
   }, hooks.map(function(hook) {
      var bottom = Math.max(0, ratingY(hook.rating) - 7);
      var left = Math.max(0, clockX(hook.t) - 4);
      return m('span', {
         id: hook.id,
         key: hook.id,
         class: ["plot", hook.team].join(' '),
         style: {
            bottom: px(bottom),
            left: px(left)
         }
      });
   })),
   renderYAxis(), renderXAxis()
]);

m.render(document.getElementById('hooks_wrap'), html)
