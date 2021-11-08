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
            useListener('get_oc_ex', this.get_oc_ex);
            useListener('get_register_ex', this.get_register_ex);
            useListener('get_sag_ex', this.get_sag_ex);
        }
        is_available() {
           const order = this.env.pos.get_order();
           return order;
        }
        async get_oc_ex() {
           var order = this.env.pos.get_order();
           const { confirmed, payload: Exento } = await this.showPopup('TextInputPopup', {
               title: this.env._t('Datos del Contribuyente Exonerado'),
               body: this.env._t('N° O/C Exenta'),

           });

           if (confirmed) {
               console.log(Exento, 'Exento');
               order.note1 = Exento;
               this.get_register_ex(order);

           }
        }
        async get_register_ex(order) {
           const { confirmed, payload: Exonerado  } = await this.showPopup('TextInputPopup', {
               title: this.env._t('Datos del Contribuyente Exonerado'),
               body: this.env._t('N° Registro Exonerado'),

           });

           if (confirmed) {
               console.log(Exonerado, 'Exonerado');
               order.note2 = Exonerado;
               this.get_sag_ex(order);
           }
        }
        async get_sag_ex(order) {
           const { confirmed, payload: SAG } = await this.showPopup('TextInputPopup', {
               title: this.env._t('Datos del Contribuyente Exonerado'),
               body: this.env._t('N° Registro SAG'),

           });

           if (confirmed) {
               console.log(SAG, 'SAG');
               order.note3 = SAG;
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