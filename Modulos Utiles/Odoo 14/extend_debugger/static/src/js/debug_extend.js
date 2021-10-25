odoo.define('extender.DebugManager.Backend', function (require) {
"use strict";

var core = require('web.core');
var DebugManager = require('web.DebugManager');
var _t = core._t;
/**
 * add new meodoo.define('extender.DebugManager.Backend', function (require) {
"use strict";

var core = require('web.core');
var DebugManager = require('web.DebugManager');
var _t = core._t;
/**
 * add new methods available for the debug manager
 */
DebugManager.include({
    get_action_menu () {
    var modelo = $(event.target).attr('data-model');
    var name = $(event.target).attr('data-name') ? $(event.target).attr('data-name') : "Acción" ;
    if(modelo) {
     this.do_action({
            res_model: modelo,
            name: _t(name),
            views: [[false, 'list'], [false, 'form']],
            domain: [],
            type: 'ir.actions.act_window',
            context: {}
        });
        }
    },
    async get_model () {
        const modelId = await this.getModelId(this._action.res_model);
        this.do_action({
            res_model: 'ir.model',
            name: _t('Models'),
            views: [[false, 'list'], [false, 'form']],
            domain: [['id', '=', modelId]],
            type: 'ir.actions.act_window',
            context: {
            'default_id': modelId}
        });
    },

});

});
