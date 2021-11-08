odoo.define('pos_ticket_custom.pos', function (require) {
"use strict";
    var core = require('web.core');
    var models = require('point_of_sale.models');
    // var Model = require('web.DataModel');
	var add_discount_exadd_discount_ex = require('point_of_sale.popups');
	var screens = require('point_of_sale.screens');
	var gui = require('point_of_sale.gui');
    var _t = core._t; 
    var QWeb = core.qweb;
    var chrome = require('point_of_sale.chrome');
    var PosBaseWidget = require('point_of_sale.BaseWidget');
    models.load_fields("pos.order", "is_tax_free_order");
    models.load_fields("pos.order", "facturacion");



models.load_models({
		model : 'ir.sequence',
		fields : [],
		domain : function(self) {
			return [['id','=',self.config.pos_order_secuencia_id[0]]];
		},
		loaded : function(self, sequence) {
			self.config.pos_order_sequence = sequence[0];
		},
	});
    var posmodel_super = models.PosModel.prototype;

    models.PosModel = models.PosModel.extend({
        push_order: function(order){
            var current_screen = this.gui.get_current_screen();
            var name_custom = this.sequence_next(this.config.pos_order_sequence);
            if(this.get_order() && current_screen == "payment"){
                this.get_order().facturacion = name_custom;
            }
            var pushed = posmodel_super.push_order.call(this, order);
            return pushed;
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

        },
        export_for_printing: function(){
            var data = _super_order.export_for_printing.apply(this, arguments);
            data.note1 = this.note1;
            data.note2 = this.note2;
            data.note3 = this.note3;
            data.facturacion = this.facturacion;
            data.is_tax_free_order=this.is_tax_free_order;
            data.exento=this.exento;
            return data;
        }
    });




    var PosCustNotePopupWidget = add_discount_exadd_discount_ex.extend({
    template: 'PosCustNotePopupWidget',
        renderElement: function(){
            this._super(); 
            var self = this;
            $(".save_order_line_note").click(function(){

                var order = self.pos.get('selectedOrder');
                order.note1 = $(".order_line_note1").val();
                order.note2 = $(".order_line_note2").val();
                order.note3 = $(".order_line_note3").val();
                self.gui.show_screen('products');

            });
        },
        show: function(options){
            var self = this;
            this.options = options || {};
            this.options.wv_order_note = self.pos.wv_order_note;
            this._super(options); 
            this.renderElement();
        },
    });
    gui.define_popup({
        'name': 'pos-cust-note-popup', 
        'widget': PosCustNotePopupWidget,
    });



    /*
    var OrderNoteExButton = screens.ActionButtonWidget.extend({
        template: 'OrderNoteExButton',
        button_click: function(){
            var self = this;
            var order = self.pos.get_order();
            if(order){
                self.gui.show_popup('pos-cust-note-popup',{'order':order});
            }
        },
    });

    screens.define_action_button({
        'name': 'order_ex_note',
        'widget': OrderNoteExButton,
        'condition': function(){
            return true; //this.pos.config.allow_order_note;
        },
    });
    */

    /////////////////////////////////////////////////////////////////////////////
    add_discount_exadd_discount_ex.include({
        renderElement: function(){
            var self = this;
            this._super();
            this.$('.add-Contribuyente').click(function(event){
                var order = self.pos.get_order();
                if(order){
                    self.gui.show_popup('pos-cust-note-popup',{'order':order});
                }
            });

        },
    });
    /////////////////////////////////////////////////////////////////////////////

    // Modificacion a Date para calcular fecha sin las horas
    Date.prototype.withoutTime = function(){
        var d = new Date(this);
        d.setHours(0,0,0,0);
        return d;
    }

    // Modificacion a Date para agregar dias a una fecha
    Date.prototype.addDays = function(days){
        var d = new Date(this.valueOf());
        d.setDate(d.getDate() + days);
        return d;
    }

    //Alertas para evitar facturar con el cai vencido!
     screens.ActionpadWidget.include({

        //Validacion del CAI
        validate_cai: function(maximo, numero_actual, fecha_exp){
            // Convertir fecha de expiracion para comparar sin horas
            var exp_date = fecha_exp.split('-');
            exp_date = new Date(exp_date[0], exp_date[1] - 1, exp_date[2]);
            exp_date = exp_date.withoutTime();

            // Fecha actual Sin horas
            var date = new Date();
            date = date.withoutTime();

            //Validacion!
            if(numero_actual > maximo || date > exp_date ){
                return "caduco";
            }else if (numero_actual + 10 > maximo || date.addDays(2) > exp_date){
                return "proximo_a_caducar";
            }else {
                return "falta";
            }
        },

        //Funcion original modificada
        renderElement: function() {
        var self = this;
        this._super();
        this.$('.pay').click(function(){

            var order = self.pos.get_order();
            var has_valid_product_lot = _.every(order.orderlines.models, function(line){
                return line.has_valid_product_lot();
            });

            // Obtener valores para la validacion!
            var maximo = self.pos.config.rango_maximo;
            var fecha_exp = self.pos.config.fecha_expiracion;
            var numero_actual = self.pos.config.pos_order_sequence.number_next_actual - 1;

            // Realizar valdacion!
            var has_valid_cai = self.validate_cai(maximo, numero_actual, fecha_exp);

            // analisis del resultado de la validacion!
            if( has_valid_cai === "caduco" ){
                 self.gui.show_screen('products');
                 self.gui.show_popup('confirm',{
                        'title': _t('Imposible generar factura'),
                        'body':  _t('Ha llegado al rango máximo de impresión Autorizado o la fecha máxima de impresión expiró, favor revisar la configuración'),
                        confirm: function(){
                            self.gui.show_screen('products');
                        },
                    });
            } else if (has_valid_cai === "proximo_a_caducar"){
                self.gui.show_popup('confirm',{
                    'title': _t('¡Advertencia!'),
                    'body':  _t('está llegando al rango máximo de facturación o su CAI está a punto de expirar!'),
                    confirm: function(){
                        self.gui.show_screen('payment');
                    },
                });
            } else {
                 if(!has_valid_product_lot){
                    self.gui.show_popup('confirm',{
                        'title': _t('Empty Serial/Lot Number'),
                        'body':  _t('One or more product(s) required serial/lot number.'),
                        confirm: function(){
                            self.gui.show_screen('payment');
                        },
                    });
                }else{
                    self.gui.show_screen('payment');
                }
            }
        });
        this.$('.set-customer').click(function(){
            self.gui.show_screen('clientlist');
        });
    },
    });

});
