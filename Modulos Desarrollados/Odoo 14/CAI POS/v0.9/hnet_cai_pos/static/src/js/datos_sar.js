/*
    @author ebenedetto@hnetw.com - HNET
    @date 26/07/2021
    @decription Obtener los datos del exonerado a través de TextInputPopups
    @name_file datos_sar.js
    @version 0.8
*/

 odoo.define('datos_sar.SarData', function(require) {
'use strict';

    const { Gui } = require('point_of_sale.Gui');
    const PosComponent = require('point_of_sale.PosComponent');
    const { posbus } = require('point_of_sale.utils');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');
    const PaymentScreen = require('point_of_sale.PaymentScreen');

    // Boton para registrar datos del exonerado
    class SarData extends PosComponent {
        constructor() {
            super(...arguments);
            useListener('click', this.get_oc_ex);
            useListener('get_register_ex', this.get_register_ex);
            useListener('get_sag_ex', this.get_sag_ex);
        }
        is_available() {
           const order = this.env.pos.get_order();
           return order;
        }
        async get_oc_ex() {
           var order = this.env.pos.get_order();
           var orderlines = order.get_orderlines();
           var client = this.env.pos.get_client();

           if (orderlines.length != 0 & client != null){
               const { confirmed, payload: Exento } = await this.showPopup('TextInputPopup', {
               title: this.env._t('Datos del Contribuyente Exonerado'),
               body: this.env._t('N° O/C Exenta'),
               value: '',

               });

               if (confirmed) {
                   order.note1 = Exento;
                   this.get_register_ex(order);

               }
           }else{
               alert('Debe agregar productos a la orden y escoger un cliente antes de definir los datos del exonerado');
           }

        }
        async get_register_ex(order) {
           const { confirmed, payload: Exonerado  } = await this.showPopup('TextInputPopup', {
               title: this.env._t('Datos del Contribuyente Exonerado'),
               body: this.env._t('N° Registro Exonerado'),
               value: '',

           });

           if (confirmed) {
               order.note2 = Exonerado;
               this.get_sag_ex(order);
           }

        }
        async get_sag_ex(order) {
           const { confirmed, payload: SAG } = await this.showPopup('TextInputPopup', {
               title: this.env._t('Datos del Contribuyente Exonerado'),
               body: this.env._t('N° Registro SAG'),
               value: '',

           });

           if (confirmed) {
               order.note3 = SAG;
           }
        }
        //--------------------------------------------------------------------------
        //  VALIDACION DEL CAI
        validate_cai(maximo, numero_actual, fecha_exp){
            // Convertir fecha de expiracion para comparar sin horas
            var exp_date = fecha_exp.split('-');
            exp_date = new Date(exp_date[0], exp_date[1] - 1, exp_date[2]);
            exp_date = exp_date.withoutTime();

            // Fecha actual Sin horas
            var date = new Date();
            date = this.withoutTime();

            //Validacion!
            if(numero_actual > maximo || date > exp_date ){
                return "caduco";
            }else if (numero_actual + 10 > maximo || this.addDays(2) > exp_date){
                return "proximo_a_caducar";
            }else {
                return "falta";
            }
        }
        withoutTime(){
            var d = new Date(this);
            d.setHours(0,0,0,0);
            return d;
        }
        // Modificacion a Date para agregar dias a una fecha
        addDays(days){
            var d = new Date(this.valueOf());
            d.setDate(d.getDate() + days);
            return d;
        }
        //Funcion original modificada
        renderElement() {
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

    }

    }
    SarData.template = 'SarData';

    ProductScreen.addControlButton({
        component: SarData,
        condition: function() {
            return this.env.pos;
        },
        position: ['before', 'SetPricelistButton'],
    });

    Registries.Component.add(SarData);

    return SarData;
});