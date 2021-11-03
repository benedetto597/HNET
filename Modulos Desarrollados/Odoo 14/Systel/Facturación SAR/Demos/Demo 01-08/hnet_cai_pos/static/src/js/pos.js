/*
    @author ebenedetto@hnetw.com - HNET
    @date 27/07/2021
    @decription Asignación de campos a la factura - Validaciones
    @name_file pos.js
    @version 1.0
*/

odoo.define('pos_ticket_custom.pos', function (require) {
"use strict";
    var core = require('web.core');
    var models = require('point_of_sale.models');
    // var Model = require('web.DataModel');
	// var screens = require('point_of_sale.screens');
	const {gui} = require('point_of_sale.Gui');
    var _t = core._t; 
    var QWeb = core.qweb;
    var rpc = require('web.rpc');
    var {chrome} = require('point_of_sale.Chrome');
    models.load_fields("pos.order", "is_tax_free_order");
    models.load_fields("pos.order", "facturacion");

models.load_models({
		model : 'ir.sequence',
		fields : [],
		domain : function(self) {
			return [['id','=',self.config.pos_order_sequence_id[0]]];
		},
		loaded : function(self, sequence) {
            self.config.pos_order_sequence = sequence[0];
		},

	});


    var posmodel_super = models.PosModel.prototype;

    models.PosModel = models.PosModel.extend({
        push_order: function(order){
            var name_custom = this.sequence_next(this.config.pos_order_sequence);
            if(this.get_order()){
                this.get_order().facturacion = name_custom;
                this.get_order().name = name_custom;
            }
        },

	sequence_next: function(seq){
		var idict = {
		    'year': moment().format('YYYY'),
		    'month': moment().format('MM'),
		    'day': moment().format('DD'),
		    'y': moment().format('YY')
		}
		var format = function(s, dict){
		    s = s || '';
		    $.each(dict, function(k, v){
		        s = s.replace('%('+k+')s', v)
		    })
		    return s;
		};
		function pad(n, width, z) {
		    z = z || '0';
		    n = n + '';
		    return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
		}
		var num = seq.number_next_actual - seq.number_increment;
		seq.number_next_actual += seq.number_increment;
		return format(seq.prefix, idict) + pad(num, seq.padding) + format(seq.suffix, idict)
        }
    });

    var _super_order = models.Order.prototype;
    models.Order = models.Order.extend({
        initialize: function(attr, options) {

            _super_order.initialize.call(this,attr,options);
            this.note1 = this.note1 || "";
            this.note2 = this.note2 || "";
            this.note3 = this.note3 || "";
            this.facturacion = this.facturacion || "";
            this.exento = this.exento || "0.00";
            this.tax_15 = this.tax_15 || "0.00";
            this.tax_18 = this.tax_18 || "0.00";
            this.tax_bf1 = this.tax_bf1 || "0.00";
            this.tax_bf2 = this.tax_bf2 || "0.00";
            this.tax_bf3 = this.tax_bf3 || "0.00";
        },
        set_extra_note: function(note){
            this.note1 = note.note1 || "";
            this.note2 = note.note2 || "";
            this.note3 = note.note3 || "";
        },
        export_as_JSON: function(){
            var json = _super_order.export_as_JSON.call(this);
            json.note1 = this.note1;
            json.note2 = this.note2;
            json.note3 = this.note3;
            json.facturacion = this.facturacion;
            json.is_tax_free_order = this.is_tax_free_order;
            json.exento = this.exento;
            json.tax_15 = this.tax_15;
            json.tax_18 = this.tax_18;
            json.tax_bf1 = this.tax_bf1;
            json.tax_bf2 = this.tax_bf2;
            json.tax_bf3 = this.tax_bf3;

            return json;
        },
        init_from_JSON: function(json){
            _super_order.init_from_JSON.apply(this,arguments);
            this.note1 = json.note1;
            this.note2 = json.note2;
            this.note3 = json.note3;
            this.facturacion = json.facturacion;
            this.is_tax_free_order=json.is_tax_free_order;
            this.exento=json.exento;
            this.tax_15 = json.tax_15;
            this.tax_18 = json.tax_18;
            this.tax_bf1 = json.tax_bf1;
            this.tax_bf2 = json.tax_bf2;
            this.tax_bf3 = json.tax_bf3;

        },
        export_for_printing: function(){
            var data = _super_order.export_for_printing.apply(this, arguments);
            data.note1 = this.note1;
            data.note2 = this.note2;
            data.note3 = this.note3;
            data.facturacion = this.facturacion;
            data.is_tax_free_order=this.is_tax_free_order;
            data.exento=this.exento;
            data.tax_15 = this.tax_15;
            data.tax_18 = this.tax_18;
            data.tax_bf1 = this.tax_bf1;
            data.tax_bf2 = this.tax_bf2;
            data.tax_bf3 = this.tax_bf3;

            return data;
        },

    });
});
