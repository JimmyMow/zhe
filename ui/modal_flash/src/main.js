var m = require('mithril');
var el = document.getElementById("flash_modal");

function modal(cl, msg) {
   if(!document.getElementById("flash_modal")) {
      el = document.createElement('div');
      el.id = 'flash_modal';
      el.className = "z-9000";
      document.body.appendChild(el);
   }
   var html = m('div', { config: fadesIn, class: 'overlay_flash', id: "modal", style: { display: 'block', opacity: 1 }, onclick: function() {
         this.remove();
         el.remove();
      }
   },
      m('div', { class: 'modal_cancel' },
         m('div', { class: ['modal_content', 'flash'].join(' ') },
            m('div', { class: 'flash_header' },
               m('span', { class: 'modal__cancel' },
                  m('i', { class: 'fa fa-times' })
               ),
               m('div', { class: 'flash_icon' },
                  m('i', { class: cl === 'error' ? 'fa fa-times-circle' : 'fa fa-check-circle' })
               ),
               m('h2', { class: ['flash_title', cl === 'error' ? 'error' : 'success'].join(' ') }, cl === 'error' ? 'Uh Oh...' : 'Yay!')
            ),
            m('p', { class: 'flash_message' }, msg)
         )
      )
   )
   m.render(el, html);
}

function fadesIn(el, initialized, ctx) {
  if (!initialized) {
    $(el).fadeIn()
  }
}

module.exports = {
   modal: modal
}
