var m = require('mithril');
var utils = require('./utils.js');
var history = document.getElementById("history");

function buildTransactions(txs, usd_price) {
   var html = m('div', {
      class: ['transactions_container'],
   },
   m('h3', 'Your transaction history'),
   txs.map(function(tx) {
         var btc_amount = zheWallet.satoshiToBtc(tx.amount);
         var usd_amount = (usd_price * btc_amount).toFixed(2);

         var type = null;
         for (var i=0; i < tx.outs.length; i++) {
            if ( zheWallet.getWallet().addresses.indexOf(tx.outs[i].address) > -1 ) {
               type = "Received bitcoin";
            }
         }
         if (!type) { type = "Sent bitcoin"; }

         return m('div', { class: 'tx' },
            m('div', { class: 'tx_left' },
               m('div', { class: 'tx_date' },
                  m('span', { class: 'tx_month' }, utils.formatTimestamp(tx.timestamp, '%b')),
                  m('span', { class: 'tx_day' }, utils.formatTimestamp(tx.timestamp, '%d'))
               ),
               // <div class="icon-wrapper">
                  // <i class="fa fa-bar-chart custom-icon">
                  //    <span class="fix-editor">&nbsp;</span>
                  // </i>
               // </div>
               m('div', { class: 'icon' },
                  m('div', { class: 'icon-wrapper' },
                     m('a', { href: "https://blockexplorer.com/tx/" + tx.id, target: "_blank" },
                        m('i', { class: [type == 'Received bitcoin' ? 'fa fa-download' : 'fa fa-hand-o-left', 'custom-icon'].join(' ') },
                           m('span', { class: 'fix-editor' }, "&nbsp;")
                        )
                     )
                  )
               )
            ),
            m('div', { class: 'tx_right' },
               m('div', { class: 'tx_detail' },
                  m('span', { class: 'msg' }, type),
                  m('span', { class: 'confirmations' }, tx.confirmations > 0 ? "Confirmations: " + tx.confirmations : "Pending...")
               ),
               m('div', { class: 'tx_amount' },
                  m('div', { class: 'tx_amount_wrapper' },
                     m('span', { class: 'amount_btc' }, "Ƀ " + btc_amount),
                     m('span', { class: 'amount_usd' }, "$ " +  usd_amount)
                  )
               )
            )
         );
      })
   );

   m.render(history, html);
}
module.exports = {
   buildTransactions: buildTransactions
}
