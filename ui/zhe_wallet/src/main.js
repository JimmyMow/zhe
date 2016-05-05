var work = require('webworkify');
var worker = work(require('./worker.js'));
var rng = require('secure-random').randomBuffer;
var Wallet = require('cb-wallet');
var crypto = require('crypto');

var wallet = null;
var seed = null;
var id = null;

var wallets = [
   {id: '820cf6de0821b8783f986cb9bb7a3aeccbae7bbf13e0bec02458e32950c43b36'},
   {id: '6ed231e67f7dc46078ae21132e54de300bded5fa9bf867c7bbaa178ba7cb32eb'}
];

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
      for (var i=0; i < wallets.length; i++) {
         console.log(wallets[i].id);
         if(wallets[i].id === id) {
            console.log("its a match!!!!!!");
            callback(null, { userExists: true, seed: seed, mnemonic: mnemonic, _id: id });
            return;
         }
      }
      callback(null, {userExists: false, seed: e.data.seed, mnemonic: mnemonic, _id: id});
   }, false)
}

function initWallet(externalAccount, internalAccount, networkName, done, unspentsDone, balanceDone){
  wallet = new Wallet(externalAccount, internalAccount, networkName, function(err, w) {
    if(err) return done(err)

    var txObjs = wallet.getTransactionHistory()
    console.log("txs: ", txObjs);
    done(null, txObjs.map(function(tx) {
      return parseTx(wallet, tx)
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
        address: bitcoin.address.fromOutputScript(output.script.chunks, network).toString(),
        amount: output.value
      };
      return obj;
    })
  }
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
   bitcoin: bitcoin
};


