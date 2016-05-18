$(document).ready(function() {
   countdown.start("countdown", deadline);

   $('.fund_bet').on('submit', function(e) {
      var passphrase = prompt("Please enter your passphrase");
      if(!passphrase) { console.log("passphrase is null: ", passphrase); return false; }

      $('.wager_show div.lichess_overboard').addClass('active');

      var script_address = $(this).data("address");
      var owe_usd = $(this).data('owe');
      var owe_btc = zheWallet.usdToBtc(owe_usd);

      console.log(passphrase);
      zheWallet.createWallet(passphrase, 'bitcoin', function(err, data) {
         var accountZero = bitcoin.HDNode.fromSeedHex(data.seed, bitcoin.networks['bitcoin']).deriveHardened(0);
         console.log(accountZero);
         zheWallet.initWallet(accountZero.derive(0), accountZero.derive(1), 'bitcoin', function(err, data) {
            if (err) {
               console.log("error on initWallet: ", err);
               modal_flash.modal('right', "error", "There was a problem initializing your wallet")
               return;
            }
            var wallet = zheWallet.getWallet();
            var to = script_address;
            var amount = owe_btc;

            zheWallet.validateSend(wallet, to, amount, parseInt(fee_pb), function(err, fee) {
               if(err) {
                  var interpolations = err.interpolations
                  if(err.message.match(/trying to empty your wallet/)){
                     modal_flash.modal('right', 'error', err.message);
                     return;
                  }

                  modal_flash.modal('right', 'error', err.message);
                  return;
               }

               var satoshis = zheWallet.btcToSatoshi(amount);
               var tx = null;

               try {
                  tx = wallet.createTx(to, satoshis, parseInt(fee_pb))
               } catch(err) {
                  console.log("err: ", err);
                  var e = err.message || "There was an error";
                  modal_flash.modal('right', "error", e)
               }

               var url = "https://blockexplorer.com/api/tx/send";
               $.ajax({
                  type: "POST",
                  url: url,
                  data: {
                  "rawtx": tx.toHex()
               },
               success: function(data) {
                  $.ajax({
                     url: '/transaction',
                     method: 'POST',
                     data: {
                        "tx_id": data.txid,
                        "wager_id": window.location.pathname.split("/")[window.location.pathname.split("/").length - 1]
                     },
                     success: function(tx) {
                        console.log("tx: ", tx);
                        window.location.reload();
                     },
                     error: function(error) {
                        console.log("error: ", error);
                     }
                  });
                  wallet.processTx(tx);
               },
               error:  function(e) {
                  var e = err.message || "There was an error";
                  modal_flash.modal('right', "error", e)
               }
               });
            });
         }, null, null);
      });
      e.preventDefault();
      return false;
   });
});
