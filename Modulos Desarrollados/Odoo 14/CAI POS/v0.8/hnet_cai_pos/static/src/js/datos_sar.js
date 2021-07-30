/*
    @author ebenedetto@hnetw.com - HNET
    @date 26/07/2021
    @decription Obtener los datos del exonerado a través de TextInputPopups
    @name_file datos_sar.js
    @version 1.0
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
           if (orderlines.length != 0){
               const { confirmed, payload: Exento } = await this.showPopup('TextInputPopup', {
               title: this.env._t('Datos del Contribuyente Exonerado'),
               body: this.env._t('N° O/C Exenta'),

               });

               if (confirmed) {
                   order.note1 = Exento;
                   this.get_register_ex(order);

               }
           }else{
               alert('Debe agregar productos a la orden antes de definir los datos del exonerado');
           }

        }
        async get_register_ex(order) {
           const { confirmed, payload: Exonerado  } = await this.showPopup('TextInputPopup', {
               title: this.env._t('Datos del Contribuyente Exonerado'),
               body: this.env._t('N° Registro Exonerado'),

           });

           if (confirmed) {
               order.note2 = Exonerado;
               this.get_sag_ex(order);
           }else{
               order.note1 = '';
               order.note2 = '';
           }

        }
        async get_sag_ex(order) {
           const { confirmed, payload: SAG } = await this.showPopup('TextInputPopup', {
               title: this.env._t('Datos del Contribuyente Exonerado'),
               body: this.env._t('N° Registro SAG'),

           });

           if (confirmed) {
               order.note3 = SAG;
           }else{
               order.note1 = '';
               order.note2 = '';
               order.note3 = '';
           }
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