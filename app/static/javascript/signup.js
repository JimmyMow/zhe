$(document).ready(function() {
   var Hive = zheWallet;
   console.log(Hive);

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
         alert("Please store this! If you lose this you cannot sign and access your wallet!\n"+data.mnemonic);
      }
      var accountZero = bitcoin.HDNode.fromSeedHex(data.seed, bitcoin.networks['bitcoin']).deriveHardened(0);

      console.log("0: ", accountZero.derive(0));
      console.log("1: ", accountZero.derive(1));

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
         console.log("derive 0: ", w.externalAccount.derive(0).getAddress() === "1d9AHsVCMEtioELkr4YJW3Uj2r4pnr23A")
         console.log("derive 1: ", w.externalAccount.derive(1).getAddress() === "1H8QjRiSuK7ae5LfaP5TSWUE98ySEe9KeG")
         console.log("derive 2: ", w.externalAccount.derive(2).getAddress() === "1KEvPo9A9Z6Q3J5WQWqSfuoK3t2mCrXKFJ")
         console.log("------------------------------------------------------------------------------------------------")
         console.log("pubkey derive 0: ", getPubkey(w.externalAccount.derive(0)) === "032ae5b2a77af91f84999012d410187eb68c7ab6a6f0412d87b5fc0f9272219d07")
         console.log("privkey derive 0: ", w.externalAccount.derive(0).keyPair.toWIF() === "L2yUuYVYFPSsjFC6LfE2AtRhWyC5NGCRUFatXMJgCZcz83TXv7Mm")
         console.log(w);
      }, unspentsDone, balanceDone);

   });
});
