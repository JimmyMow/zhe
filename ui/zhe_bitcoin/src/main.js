var bitcoin = require('bitcoinjs-lib');

var exports = {};

exports.createPair = function() {
   var ecPair = bitcoin.ECPair.makeRandom();
   var keypair = {};
   keypair.pubkey = ecPair.Q.getEncoded().toString('hex');;
   keypair.privkey = ecPair.toWIF();
   keypair.address = ecPair.getAddress();

   return keypair;
};

exports.userDownload = function(filename, keypair) {
   var text = "Public key: " + keypair.pubkey + "\nPrivate key: " + keypair.privkey;
   var element = document.createElement('a');
   element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
   element.setAttribute('download', filename);

   element.style.display = 'none';
   document.body.appendChild(element);

   element.click();

   document.body.removeChild(element);
}

module.exports = exports;
