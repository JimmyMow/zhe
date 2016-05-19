$(document).ready(function() {
   var tx = bitcoin.Transaction.fromHex(tx_hex);
   var tx_builder = bitcoin.TransactionBuilder.fromTransaction(tx);

   console.log(tx_builder);

   $("#sign_passphrase").on("submit", function(e) {
      var passphrase = $(this).find('input').val();
      if(!passphrase) { return; }
      $(this).find('input').val('');

      zheWallet.createWallet(passphrase, 'bitcoin', function(err, data) {
         var accountZero = bitcoin.HDNode.fromSeedHex(data.seed, bitcoin.networks['bitcoin']).deriveHardened(0);
         if (data._id != home_seed && data._id != away_seed) {
            modal_flash.modal('right', "error", "Your wallet passphrase is incorrect");
            return;
         }

         var user_team = data._id == home_seed ? 'home' : 'away';

         zheWallet.initWallet(accountZero.derive(0), accountZero.derive(1), 'bitcoin', function(err, data) {
            if (err) {
               console.log("error on initWallet: ", err);
               modal_flash.modal('right', "error", "There was a problem initializing your wallet")
               return;
            }
            var w = zheWallet.getWallet();
            var derive_index = user_team === 'home' ? parseInt(home_derive_index) : parseInt(away_derive_index);
            console.log(derive_index)
            var keyPair = w.externalAccount.derive(derive_index).keyPair;

            for (var i=0; i < tx_builder.inputs.length; i++) {
               tx_builder.sign(i, keyPair);
            }

            var tx_hex = tx_builder.build().toHex();

            var url = "https://blockexplorer.com/api/tx/send";
            $.ajax({
               type: "POST",
               url: url,
               data: {
               "rawtx": tx_hex
            },
            success: function(d) {
               modal_flash.modal("right", "success", "You sent the money to the winner")
               console.log("txid: ", d);
            },
            error: function(e) {
               modal_flash.modal("right", "error", "Problem broadcasting tx")
            }
            });
         });
      });
      e.preventDefault();
      return false;
   });
});
