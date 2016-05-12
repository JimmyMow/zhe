'use strict';

var networks = require('bitcoinjs-lib').networks
var btcToSatoshi = convert.btcToSatoshi
var satoshiToBtc = convert.satoshiToBtc

function validateSend(wallet, to, btcValue, fee_pb, callback){
  console.log("hey we made it to validateSend");
  var amount = btcToSatoshi(btcValue)
  var network = networks[wallet.networkName]
  var tx = null

  console.log("amount: ", amount);
  console.log("network: ", network);
  console.log("tx: ", tx);

  try {
    tx = wallet.createTx(to, amount, fee_pb);
  } catch(e) {
    console.log("e: ", e);
    if(e.message.match(/Invalid address/)) {
      return callback(new Error('Please enter a valid address to send to'))
    } else if(e.message.match(/Invalid value/)) {
      var error = new Error('Please enter an amount above')
      error.interpolations = { dust: satoshiToBtc(e.dustThreshold) }
      return new callback(error)
    } else if(e.message.match(/Insufficient funds/)) {
      var error

      if(e.details && e.details.match(/Additional funds confirmation pending/)){
        error = new Error("Some funds are temporarily unavailable. To send this transaction, you will need to wait for your pending transactions to be confirmed first (this should not take more than a few minutes).")
        error.href = "https://github.com/hivewallet/hive-osx/wiki/Sending-Bitcoin-from-a-pending-transaction"
        error.linkText = "What does this mean?"
        return callback(error)
      } else if(attemptToEmptyWallet(wallet.getBalance(), amount, network)){
        var message = [
          "It seems like you are trying to empty your wallet",
          "Taking transaction fee into account, we estimated that the max amount you can send is",
          "We have amended the value in the amount field for you"
        ].join('. ')
        error = new Error(message)

        var sendableBalance = satoshiToBtc(amount - (e.needed - e.has))
        error.interpolations = { sendableBalance: sendableBalance }

        return new callback(error)
      } else {
        return callback(new Error("You do not have enough funds in your wallet"))
      }
    }
    return new callback(e)
  }
  console.log("tx? lol ", tx);
  var estimated_fee = calcFee(tx, fee_pb);
  callback(null, estimated_fee)

}

function calcFee(tx, fee_pb) {
  var res = tx.byteLength() * fee_pb;
  if(!res ) { console.log("woah wtf"); return; }

  return res;
}

function attemptToEmptyWallet(balance, amount, network){
  return balance - network.feePerKb < amount && amount <= balance
}

module.exports = validateSend;
