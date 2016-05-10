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
            m('div', { class: 'tx_header' }, utils.formatTimestamp(tx.timestamp)),
            m('div', { class: 'icon' },
               m('i', { class: type == 'Received bitcoin' ? 'fa fa-hand-o-right' : 'fa fa-hand-o-left' })
            ),
            m('div', { class: 'tx_left' },
               m('span', { class: 'msg' }, type),
               m('span', { class: 'confirmations' }, tx.confirmations > 0 ? "Confirmations: " + tx.confirmations : "Pending...")
            ),
            m('div', { class: 'tx_right' },
               m('span', { class: 'amount_satoshis' }, "Ƀ " + btc_amount),
               m('span', { class: 'amount_usd' }, "$ " +  usd_amount)
            )
         );
      })
   );

   m.render(history, html);
}
module.exports = {
   buildTransactions: buildTransactions
}
