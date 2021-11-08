odoo.define('aplicar_descuento_sar.SarData', function (require) {
    "use strict";


        const { Gui } = require('point_of_sale.Gui');
        const PosComponent = require('point_of_sale.PosComponent');
        const { posbus } = require('point_of_sale.utils');
        const ProductScreen = require('point_of_sale.ProductScreen');
        const { useListener } = require('web.custom_hooks');
        const Registries = require('point_of_sale.Registries');
        const PaymentScreen = require('point_of_sale.PaymentScreen');

        ////////////////////////////////////////////////
        /*Aplicar el descuento si es exonerado*/
        ///////////////////////////////////////////////
        class CstmPaymentScreen extends PaymentScreen {
            constructor() {
                super(...arguments);
                useListener('add_discount_ex', this.add_discount_ex);
            }
            add_discount_ex(){
                this.pos.get_order().clean_empty_paymentlines();
                var order = this.pos.get_order();
                if(order.note1.length ||order.note2.length || order.note3.length){
                        order.is_tax_free_order = false;
                        var ext = 0 ;
                        var orderlines = order.get_orderlines();
                        $.each(orderlines,function(index){
                            var line = orderlines[index];
                            line.price = line.product.lst_price;
                            ext += line.get_tax();
                            line.price = line.get_price_without_tax();
                            line.trigger('change',line);
                        });
                        order.exento = ext;
                        order.is_tax_free_order = true;
                    }else{
                        order.is_tax_free_order=false;
                    }
                this.reset_input();
                this.render_paymentlines();
                // that one comes from BarcodeEvents
                $('body').keypress(this.keyboard_handler);
                // that one comes from the pos, but we prefer to cover all the basis
                $('body').keydown(this.keyboard_keydown_handler);
            }
        }
        CstmPaymentScreen.template = 'CstmPaymentScreen';
        Registries.Component.add(CstmPaymentScreen);
        return CstmPaymentScreen;
    });