// ==ClosureCompiler==
// @compilation_level ADVANCED_OPTIMIZATIONS
// ==/ClosureCompiler==

var zhe = window.zhe = window.zhe || {};

zhe.getParameterByName = function(name) {
  var match = RegExp('[?&]' + name + '=([^&]*)').exec(location.search);
  return match && decodeURIComponent(match[1].replace(/\+/g, ' '));
};

function withStorage(f) {
  // can throw an exception when storage is full
  try {
    return !!window.localStorage ? f(window.localStorage) : null;
  } catch (e) {}
}
zhe.storage = {
  get: function(k) {
    return withStorage(function(s) {
      return s.getItem(k);
    });
  },
  remove: function(k) {
    withStorage(function(s) {
      s.removeItem(k);
    });
  },
  set: function(k, v) {
    // removing first may help http://stackoverflow.com/questions/2603682/is-anyone-else-receiving-a-quota-exceeded-err-on-their-ipad-when-accessing-local
    withStorage(function(s) {
      s.removeItem(k);
      s.setItem(k, v);
    });
  }
};
zhe.once = function(key, mod) {
  if (mod === 'always') return true;
  if (!zhe.storage.get(key)) {
    zhe.storage.set(key, 1);
    return true;
  }
  return false;
};
zhe.trans = function(i18n) {
  return function(key) {
    var str = i18n[key] || key;
    Array.prototype.slice.call(arguments, 1).forEach(function(arg) {
      str = str.replace('%s', arg);
    });
    return str;
  };
};
zhe.widget = function(name, prototype) {
  var constructor = $[name] = function(options, element) {
    var self = this;
    self.element = $(element);
    $.data(element, name, self);
    self.options = options;
    self._create();
  };
  constructor.prototype = prototype;
  $.fn[name] = function(method) {
    var returnValue = this;
    var args = Array.prototype.slice.call(arguments, 1);
    if (typeof method === 'string') this.each(function() {
      var instance = $.data(this, name);
      if (!$.isFunction(instance[method]) || method.charAt(0) === "_")
        return $.error("no such method '" + method + "' for " + name + " widget instance");
      returnValue = instance[method].apply(instance, args);
    });
    else this.each(function() {
      if ($.data(this, name)) return $.error("widget " + name + " already bound to " + this);
      $.data(this, name, new constructor(method, this));
    });
    return returnValue;
  };
};
zhe.isTrident = navigator.userAgent.indexOf('Trident/') > -1;
zhe.isChrome = navigator.userAgent.indexOf('Chrome/') > -1;
zhe.isSafari = navigator.userAgent.indexOf('Safari/') > -1 && !zhe.isChrome;
zhe.spinnerHtml = '<div class="spinner"><svg viewBox="0 0 40 40"><circle cx=20 cy=20 r=18 fill="none"></circle></svg></div>';
zhe.assetUrl = function(url, noVersion) {
  return $('body').data('asset-url') + url + (noVersion ? '' : '?v=' + $('body').data('asset-version'));
};
zhe.loadCss = function(url) {
  $('head').append($('<link rel="stylesheet" type="text/css" />').attr('href', zhe.assetUrl(url)));
}
zhe.loadScript = function(url, noVersion) {
  return $.ajax({
    dataType: "script",
    cache: true,
    url: zhe.assetUrl(url, noVersion)
  });
};

zhe.isPageVisible = document.visibilityState !== 'hidden';
zhe.notifications = [];
// using document.hidden doesn't entirely work because it may return false if the window is not minimized but covered by other applications
window.addEventListener('focus', function() {
  zhe.isPageVisible = true;
  zhe.notifications.forEach(function(n) {
    n.close();
  });
  zhe.notifications = [];
});
window.addEventListener('blur', function() {
  zhe.isPageVisible = false;
});
zhe.unique = function(xs) {
  return xs.filter(function(x, i) {
    return xs.indexOf(x) === i;
  });
};
zhe.numberFormat = (function() {
  if (window.Intl && Intl.NumberFormat) {
    var formatter = new Intl.NumberFormat();
    return function(n) {
      return formatter.format(n);
    }
  }
  return function(n) {
    return n;
  };
})();
