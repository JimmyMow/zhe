$(document).ready(function() {
   var Hive = zheWallet;
   var showFiat = false;
   var btcToSatoshi = convert.btcToSatoshi
   var satoshiToBtc = convert.satoshiToBtc
   var rates = {};
   $.get("https://api.bitcoinaverage.com/ticker/USD/", function(data) {
      if(!data.last) {
         rates.USD = null;
         return;
      }
      rates.USD = data.last;
      return;
   });

   // Tabs
   $(".tab").on("click", function(e) {
      // Remove active classes
      $(".tab.active").removeClass('active');
      $(".wallet_content.current").removeClass('current');

      // Add classes
      $(this).addClass('active');
      $("#"+$(this).data("tab")).addClass("current");
      e.preventDefault();
      return false;
   });

   // Header balance
   $(".header_balance").on("click", function(e) {
      $(this).removeClass('btc').removeClass('usd');
      showFiat = !showFiat;
      if (showFiat) {
         var btcAmount = Hive.satoshiToBtc(Hive.getWallet().getBalance());
         Hive.btcToUsd(btcAmount, function(data) { $("#balance").text(data); });
         $(this).addClass('usd');
      } else {
         $(this).addClass('btc');
         $("#balance").text(Hive.satoshiToBtc(Hive.getWallet().getBalance()));
      }
      e.preventDefault();
      return false;
   });

   // Refresh balance
   $(".header_refresh").on("click", function(e) {
      var $spinner = $(this).find('.fa');
      $spinner.addClass('fa-spin');
      Hive.initWallet(Hive.getWallet().externalAccount, Hive.getWallet().internalAccount, 'bitcoin', function(err, data) {
         if (err) { console.log("error updating balance: ", err); return; }
         if(showFiat) {
            var btcAmount = Hive.satoshiToBtc(Hive.getWallet().getBalance());
            Hive.btcToUsd(btcAmount, function(data) { $("#balance").text(data); });
         } else {
            $("#balance").text(Hive.satoshiToBtc(Hive.getWallet().getBalance()));
         }
         $spinner.removeClass('fa-spin');
      });
      e.preventDefault();
      return false;
   });

   var unspentsDone = function(err, data) {
      console.log("err from unspentsDone: ", err);
      console.log("data from unspentsDone: ", data);
   };

   var balanceDone = function(err, data) {
      if(err) { console.log("Error on balanceDone: ", err); return; }
      $("#balance").text(Hive.satoshiToBtc(data));
   };

   $("#passphrase").on('submit', function(e) {
      $(".loader").removeClass('hidden');
      var passphrase = $(this).find('.passphrase_input').val();
      Hive.createWallet(passphrase, 'bitcoin', function(err, data) {
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
            console.log("data from init: ", data);
            $(".loader").addClass('hidden');
            $(".wallet_interface").removeClass('hidden');

            for (var i = 0; i < data.length; i++) {
               console.log("tx: ", data[i]);
            }
            $.get("https://api.bitcoinaverage.com/ticker/USD/", function(price) {
               profile.buildTransactions(data, price.last);
            });
            var w = Hive.getWallet();
            $("#address").text(w.getNextAddress());
            $("#qrcode").qrcode({
               "size": 150,
               "fill": '#000',
               "render": "div",
               "text": w.getNextAddress()
            });
            var hd = w.getHdNode(w.getNextAddress());
         }, unspentsDone, balanceDone);
      });
      $(this).find(".passphrase_input").val("");
      e.preventDefault();
   });

   // Send Form
   $("#wallet_send").on("submit", function(e) {
      var wallet = Hive.getWallet()
      var to = $("#send_btc_address").val();
      var amount = $("#send_btc_amount").val();

      if(!to || !amount) { return; }

      var tx = new bitcoin.TransactionBuilder()
      var kp = wallet.externalAccount.derive(3).keyPair;

      console.log("help: ", tx.network === kp.network);

      Hive.validateSend(wallet, to, amount, parseInt(fee_pb), function(err, fee) {
         if(err) {
            console.log("err: ", err);
         }
         console.log("to: ", to);
         console.log("amount: ", amount);
         console.log("fee: ", fee);
         var satoshis = btcToSatoshi(amount);
         var tx = null;
         console.log(satoshis);
         var x = confirm("Are you sure you want to send " + amount + "of BTC with a " + fee + " satoshi fee?");
         if(!x) { return; }

         try {
            tx = wallet.createTx(to, satoshis, parseInt(fee_pb))
         } catch(err) {
            console.log("err: ", err);
         }

         console.log("tx after remake: ", tx);
         var url = "https://blockexplorer.com/api/tx/send";
         $.ajax({
            type: "POST",
            url: url,
            data: {
               "rawtx": tx.toHex()
            },
            success: function(data) {
               console.log("data: ", data);
               wallet.processTx(tx);
               alert("Yay you sent BTC!");
            },
            error:  function(e) {
               console.log("error: ", e);
            }
         });
      });
      e.preventDefault();
      return false;
   });

   $("#wallet_send #send_btc_amount").on('keyup', function() {
      var val = $(this).val();
      if(!val.length) {
         $("#send_usd_amount").val("");
         return;
      }
      $("#send_usd_amount").val(btcToUsd(val));
   });

   $("#wallet_send #send_usd_amount").on('keyup', function() {
      var val = $(this).val();
      if(!val.length) {
         $("#send_btc_amount").val("");
         return;
      }
      $("#send_btc_amount").val(usdToBtc(val));
   });

   function btcToUsd(num_btc) {
      return (rates.USD * num_btc).toFixed(2);
   }

   function usdToBtc(num_usd) {
      return num_usd / rates.USD;
   }
});
