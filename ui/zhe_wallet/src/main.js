var work = require('webworkify');
var worker = work(require('./worker.js'));
var rng = require('secure-random').randomBuffer;
var Wallet = require('cb-wallet');
var crypto = require('crypto');
var validateSend = require('./validator');

var wallet = null;
var seed = null;
var id = null;
var rates = {};
$.get("https://api.bitcoinaverage.com/ticker/USD/", function(data) {
  if(!data.last) {
    rates.USD = null;
    return;
  }
  rates.USD = data.last;
  return;
});


function getPubkey(hd) {
   return hd.keyPair.Q.getEncoded().toString('hex');
}

function getWallet(){
  return wallet
}

function createWallet(passphrase, network, callback) {
   var data = {passphrase: passphrase}
   if(!passphrase){
      data.entropy = rng(128 / 8).toString('hex')
   }
   worker.postMessage(data);

   worker.addEventListener('message', function(e) {
      assignSeedAndId(e.data.seed)

      var mnemonic = e.data.mnemonic;
      callback(null, {userExists: false, seed: e.data.seed, mnemonic: mnemonic, _id: id});
   }, false)
}

function initWallet(externalAccount, internalAccount, networkName, done, unspentsDone, balanceDone){
  wallet = new Wallet(externalAccount, internalAccount, networkName, function(err, w) {
    if(err) return done(err)

    var txObjs = wallet.getTransactionHistory()
    done(null, txObjs.map(function(tx) {
      var parsedTx = parseTx(wallet, tx);
      return parsedTx;
    }))
  }, unspentsDone, balanceDone)

  wallet.denomination = 'BTC'
}

function parseTx(wallet, tx) {
  var id = tx.getId()
  var metadata = wallet.txMetadata[id]
  var network = bitcoin.networks[wallet.networkName]

  var timestamp = metadata.timestamp
  timestamp = timestamp ? timestamp * 1000 : new Date().getTime()

  var node = wallet.txGraph.findNodeById(id)
  var prevOutputs = node.prevNodes.reduce(function(inputs, n) {
    inputs[n.id] = n.tx.outs
    return inputs
  }, {})

  var inputs = tx.ins.map(function(input) {
    var buffer = new Buffer(input.hash)
    Array.prototype.reverse.call(buffer)
    var inputTxId = buffer.toString('hex')

    return prevOutputs[inputTxId][input.index]
  })

  return {
    id: id,
    amount: metadata.value,
    timestamp: timestamp,
    confirmations: metadata.confirmations,
    fee: metadata.fee,
    ins: parseOutputs(inputs, network),
    outs: parseOutputs(tx.outs, network)
  }

  function parseOutputs(outputs, network) {
    return outputs.map(function(output){
      var obj = {
        address: bitcoin.address.fromOutputScript(output.script, network).toString(),
        amount: output.value
      };
      return obj;
    })
  }
}

function satoshiToBtc(amount) {
  return amount / 100000000;
}

function btcToUsd(amount, done) {
  var res = parseFloat(amount) * parseFloat(rates.USD);
  return done(res.toFixed(2));
}

function usdToBtc(usd_amount) {
  var btc = usd_amount / rates.USD;
  return btc;
}

function btcToSatoshi(btc) {
  var satoshis = btc * 100000000;
  return Math.floor(satoshis);
}

function assignSeedAndId(s) {
  seed = s
  id = crypto.createHash('sha256').update(seed).digest('hex')
}

module.exports = {
   getWallet: getWallet,
   createWallet: createWallet,
   initWallet: initWallet,
   getPubkey: getPubkey,
   bitcoin: bitcoin,
   satoshiToBtc: satoshiToBtc,
   btcToUsd: btcToUsd,
   usdToBtc: usdToBtc,
   btcToSatoshi: btcToSatoshi,
   validateSend: validateSend,
   rates: rates
};


