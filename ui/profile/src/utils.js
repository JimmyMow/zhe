var strftime = require("strftime");

function formatTimestamp(timestamp) {
   var date = new Date(timestamp);
   return strftime('%b %d %l:%M %p', date);
}

module.exports = {
   formatTimestamp: formatTimestamp
}
