$(document).ready(function() {
   var Hive = zheWallet;
   console.log("Hive: ", Hive);

   var unspentsDone = function(err, data) {
      console.log("err from unspentsDone: ", err);
      console.log("data from unspentsDone: ", data);
   };

   var balanceDone = function(err, data) {
      if(err) { console.log("Error on balanceDone: ", err); return; }
      $("#balance").text(data);
   };

   Hive.createWallet('rug face primary veteran valve bless soda upper ketchup urge tone sad', 'bitcoin', function(err, data) {
      var accountZero = bitcoin.HDNode.fromSeedHex(data.seed, bitcoin.networks['bitcoin']).deriveHardened(0);
      if (data._id != wallet_seed) {
         alert("Passphrase is incorrect");
         return;
      }
      Hive.initWallet(accountZero.derive(0), accountZero.derive(1), 'bitcoin', function(err, data) {
         if (err) {
            console.log("error on initWallet: ", err);
            return;
         }

         for (var i = 0; i < data.length; i++) {
            console.log("tx: ", data[i]);
         }
         var w = Hive.getWallet();
         $("#address").text(w.getNextAddress());
         var hd = w.getHdNode(w.getNextAddress());
      }, unspentsDone, balanceDone);
   });
});
