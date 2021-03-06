$(document).ready(function() {
   // Form handlers //
   $("#user_signup").on('submit', function(e) {
      if(!$("#passhrase_checkbox").is(':checked')) {
         alert("You must check to confirm you have stored your passphrase");
         e.preventDefault();
      }
   });

   var Hive = zheWallet;

   var unspentsDone = function(err, data) {
      console.log("err from unspentsDone: ", err);
      console.log("data from unspentsDone: ", data);
   };

   var balanceDone = function(err, data) {
      if(err) { console.log("Error on balanceDone: ", err); return; }
      console.log("data from balanceDone: ", data);
   };

   Hive.createWallet(null, 'bitcoin', function(err, data) {
      console.log("create wallet callback data: ", data);
      if(!data.userExists) {
         var $passphrase = $("#passphrase");
         $passphrase.find(".passphrase").text(data.mnemonic);
         $passphrase.removeClass("hidden");
         $('.spinner').remove();
      }

      $("#wallet_seed").val(data._id);

      var accountZero = bitcoin.HDNode.fromSeedHex(data.seed, bitcoin.networks['bitcoin']).deriveHardened(0);

      console.log("0: ", accountZero.derive(0));
      console.log("1: ", accountZero.derive(1));
      console.log("encrypted thing: ", data._id);

      Hive.initWallet(accountZero.derive(0), accountZero.derive(1), 'bitcoin', function(err, data) {
         if (err) {
            console.log("error on initWallet: ", err);
            return;
         }

         for (var i = 0; i < data.length; i++) {
            console.log("tx: ", data[i]);
         }
         var w = Hive.getWallet();
         var hd = w.getHdNode(w.getNextAddress());
      }, unspentsDone, balanceDone);

   });
});
