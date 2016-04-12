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

   // zhe.socket = zhe.StrongSocket(
   //    ''
   // )

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

         var $g = $(document.getElementById("2016/04/12/pitmlb-detmlb-1"));

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
         var team_status = $bet_form.find('input[name=team]:checked').attr('id');
         if( !team_status ) { e.preventDefault(); return;}

         var data = {};
         var game_id = $('#selectGame').find(":selected").val();
         var team_name = $('label[for="' + $bet_form.find('input[name=team]:checked').attr('id') +'"]').text().toLowerCase();

         data.game_id = game_id;
         data.team_status = team_status == 'team_0' ? 'away' : 'home';
         data.team_name = team_name;
         data.value = $money.val();
         data.spread = $spread.val();
         data.line = $line.val();

         $.ajax({
            url: $(this).attr('action'),
            method: 'post',
            data: data,
            success: function(r) {
               console.log("success: ", r);
            },
            error: function(e) {
               console.log("fail: ", e);
            }
         });
         e.preventDefault();
      });
   }

   var $startButtons = $('#start_buttons');

   $startButtons.find('a').not('.disabled').click(function() {
      $(this).addClass('active').siblings().removeClass('active');
      $('.lichess_overboard').remove();
      $.ajax({
         url: $(this).attr('href'),
         success: function(html) {
            $('.lichess_overboard').remove();
            $('#hooks_wrap').prepend(html);
            prepareForm();
            // $('body').trigger('lichess.content_loaded');
         },
         error: function(e) {
            console.log("fail: ", e);
         }
      });
      return false;
   });
});
