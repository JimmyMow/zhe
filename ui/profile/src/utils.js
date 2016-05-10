var strftime = require("strftime");

function formatTimestamp(timestamp, format) {
   var date = new Date(timestamp);
   return strftime(format, date);
}

module.exports = {
   formatTimestamp: formatTimestamp
}
