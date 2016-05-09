$(document).ready(function() {
   /////////
   // Top //
   /////////
   $("#top").on("click", 'a.toggle', function() {
      var $p = $(this).parent();
      $p.toggleClass('shown');
      $p.siblings('.shown').removeClass('shown');
      setTimeout(function() {
         var handler = function(e) {
            if ($.contains($p[0], e.target)) return;
            $p.removeClass('shown');
            $('html').off('click', handler);
         };
         $('html').on('click', handler);
      }, 10);
   });

   ///////////
   // Setup //
   ///////////

   function getStringNumber(theNumber) {
       if(theNumber > 0){
           return "+" + theNumber;
       }else{
           return theNumber.toString();
       }
   }

   function calcPayout(money, odds) {
      if(odds < 0) {
         var multiplier = 100 / Math.abs(odds);
         var payout = money * multiplier;
      } else if(odds > 0) {
         var multiplier = odds / 100;
         var payout = money * multiplier;
      } else {
         var payout = money;
      }

      return payout;
   }

   function buildBetStatus(payout) {
      var $bet_form = $("#over").find('form');
      var team = $('label[for="' + $bet_form.find('input[name=team]:checked').attr('id') +'"]').text();
      if(!team) { return; }

      var line = $("#line").val() == 0 ? 'even' : $("#line").val();
      line = getStringNumber(line);

      var spread = $("#spread").val() == 0 ? 'ML' : $("#spread").val();
      spread = getStringNumber(spread);


      var status = team.charAt(0).toUpperCase() + team.slice(1) + " " + spread + " at " + line + " odds. Payout of $" + payout;
      $("#betStatus").text(status);
   }

   function prepareForm() {
      var $form = $(".lichess_overboard");
      var $bet_form = $("#over").find('form');
      var $money = $("#money");
      var $slidermoney = $("#slidermoney");
      var $spread = $("#spread");
      var $sliderspread = $("#sliderspread");
      var $line = $("#line");
      var $sliderline = $("#sliderline");
      var $selectGame = $("#selectGame");

      $selectGame.on('change', function() {
         var id = $(this).val();

         if( !id ) {
            $("#team_0").val('');
            $("#team_1").val('');
            $("label[for='team_0']").text('');
            $("label[for='team_1']").text('');
            return;
         }

         var $g = $(document.getElementById(id));

         var home_name = $g.data('homename');
         var home_id = $g.data('homeid');
         var away_name = $g.data('awayname');
         var away_id = $g.data('awayid');

         $("#team_0").val(away_id);
         $("#team_1").val(home_id);
         $("label[for='team_0']").text(away_name);
         $("label[for='team_1']").text(home_name);

         var payout = calcPayout($money.val(), $line.val());
         buildBetStatus(payout);
      });

      $money.on('change keydown keyup input', function() {
         $slidermoney.val($(this).val());
         var payout = calcPayout($money.val(), $line.val());
         buildBetStatus(payout);
      });

      $slidermoney.on('change input', function() {
         $money.val($(this).val());
         var payout = calcPayout($money.val(), $line.val());
         buildBetStatus(payout);
      });

      $spread.on('change keydown keyup input', function() {
         $sliderspread.val($(this).val());
      });

      $sliderspread.on('change input', function() {
         $spread.val($(this).val());
      });

      $line.on('change keydown keyup input', function() {
         $sliderline.val($(this).val());
         var payout = calcPayout($money.val(), $line.val());
         buildBetStatus(payout);
      });

      $sliderline.on('change input', function() {
         $line.val($(this).val());
         var payout = calcPayout($money.val(), $line.val());
         buildBetStatus(payout);
      });

      $bet_form.find('input[name=team]').on('change', function() {
         var payout = calcPayout($money.val(), $line.val());
         buildBetStatus(payout);
      });

      $form.find('a.close').click(function() {
         $form.remove();
         $startButtons.find('a.active').removeClass('active');
         return false;
      });

      $bet_form.on('submit', function(e) {
         $("#friend_loading").removeClass('hidden');
         var team_status = $bet_form.find('input[name=team]:checked').attr('id');
         var passphrase = $("#passphrase").val();
         if( !team_status || !passphrase ) {
            e.preventDefault();
            $("#friend_loading").addClass('hidden');
            return;
         }


         var data = {};
         var game_id = $('#selectGame').find(":selected").val();
         var team_name = $('label[for="' + $bet_form.find('input[name=team]:checked').attr('id') +'"]').text().toLowerCase();
         var time_date = $('#selectGame').find(":selected").attr('time-date');

         // var pair = zheBitcoin.createPair();

         // if (!pair) {
         //    alert("Problem creating your keypair. Try again");
         //    return false;
         // }

         data.game_id = game_id;
         data.team_status = team_status == 'team_0' ? 'away' : 'home';
         data.team_name = team_name;
         data.value = $money.val();
         data.spread = $spread.val();
         data.line = $line.val();
         data.time_date = time_date;
         // data.pubkey = pair.pubkey;

         zheWallet.createWallet(passphrase, 'bitcoin', function(err, d) {
            if (err) { alert("Problem with your passphrase"); return; }
            console.log("d._id ", d._id);
            console.log("user_wallet_seed ", user_wallet_seed);
            if (d._id != user_wallet_seed) {
               alert("Encrypted seed does not match the passphrase you provided. Please try again");
               $("#friend_loading").addClass('hidden');
               return;
            }
            var accountZero = bitcoin.HDNode.fromSeedHex(d.seed, bitcoin.networks['bitcoin']).deriveHardened(0);
            zheWallet.initWallet(accountZero.derive(0), accountZero.derive(1), 'bitcoin', function(err, w_d) {
               if (err) { alert("Problem with your passphrase"); return; }
               var w = zheWallet.getWallet();
               var w_pubkey = w.externalAccount.derive(w.addresses.length).keyPair.Q.getEncoded().toString('hex');
               data.pubkey = w_pubkey;
               data.derive_index = w.addresses.length;
               console.log("w_pubkey: ", w_pubkey);

               $.get("https://api.bitcoinaverage.com/ticker/USD/", function(price) {
                  if (!price.last) {
                     alert("Problem timestamping the BTC proce for your wager. Please try again.");
                     return false;
                  }

                  data.btc_stamp = price.last;
                  console.log("DATA: ", data);
                  console.log($(this));
                  $.ajax({
                     url: $('form').attr('action'),
                     method: 'post',
                     data: data,
                     success: function(data) {
                        window.location.replace("/wager/" + data.id);
                     },
                     error: function(e) {
                        console.log("fail: ", e);
                        $("#friend_loading").addClass('hidden');
                        // window.location.reload();
                     }
                  });
               }.bind(this));
            });
         }, null, null);

         e.preventDefault();
      });
   }

   var $startButtons = $('#start_buttons');

   $startButtons.find('a').not('.disabled').click(function() {
      $('#hooks_wrap').addClass('loading');
      $(this).addClass('active').siblings().removeClass('active');
      $('.lichess_overboard').remove();
      $.ajax({
         url: $(this).attr('href'),
         success: function(html) {
            $('#hooks_wrap').removeClass('loading');
            $('.lichess_overboard').remove();
            $('#hooks_wrap').prepend(html);
            prepareForm();
         },
         error: function(e) {
            $('#hooks_wrap').removeClass('loading');
            console.log("fail: ", e);
            window.location.reload();
         }
      });
      return false;
   });

   //////////////
   // Boxscore //
   //////////////

   var $accept_form = $(".wager_show").find(".accept_wager");

   $accept_form.on('submit', function(e) {
      console.log("here");
      var passphrase = prompt("Please enter your passphrase");
      console.log(passphrase);
      if(!passphrase) { console.log("passphrase is null: ", passphrase); return false; }
      zheWallet.createWallet(passphrase, 'bitcoin', function(err, d) {
         var accountZero = bitcoin.HDNode.fromSeedHex(d.seed, bitcoin.networks['bitcoin']).deriveHardened(0);
         console.log("accountZero: ", accountZero);
         zheWallet.initWallet(accountZero.derive(0), accountZero.derive(1), 'bitcoin', function(err, w_d) {
            console.log("w_d: ", w_d);
            var w = zheWallet.getWallet();
            var w_pubkey = w.externalAccount.derive(w.addresses.length).keyPair.Q.getEncoded().toString('hex');
            console.log("pubkey: ", w_pubkey);
            // p tag to be updated
            var $updated_res = $('#updated_res');
            // Add loading screen
            $('.wager_show div.lichess_overboard').addClass('active');

            var xmlhttp = new XMLHttpRequest(),
            method = "POST",
            url = window.location.pathname,
            params = "pubkey=" + w_pubkey + "&derive_index=" + w.addresses.length;
            new_res = '';

            xmlhttp.open(method, url, true);
            xmlhttp.onreadystatechange = function () {
               if(new_res.length) {
                  var x = xmlhttp.responseText.substring(new_res.length);
                  console.log("new: ", x);
                  $updated_res.text(x);
               }
               new_res = xmlhttp.responseText;
            }

            // Send request
            xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
            xmlhttp.send(params);

            // Check for incoming data
            var timer;
            timer = setInterval(function() {
               // stop checking once the response has ended
               if (xmlhttp.readyState == XMLHttpRequest.DONE) {
                  clearInterval(timer);
                  var data = xmlhttp.responseText;
                  console.log("data: ", data);
                  // window.location.reload();
               }
            }, 1000);

         });
      });

      e.preventDefault();
   });

   $("#check_funds").on("click", function(e) {
      $(this).parent('.funds_container').addClass('loading');
      var addr = $(this).attr('address');

      $.get("https://blockexplorer.com/api/addr/"+addr+"/totalReceived", function(data) {
         console.log("funds data: ", data);
         $(this).parent('.funds_container').removeClass('loading');
         $("#funds").text(data);
      }.bind(this));
      e.preventDefault();
   });
});
