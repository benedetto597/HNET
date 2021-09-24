odoo.define('hnet_cai_pos.exonerar_datos_sar', function (require) {
    "use strict";
        var core = require('web.core');
        var models = require('point_of_sale.models');

        var _super_order_line = models.Orderline.prototype;
        models.Orderline = models.Orderline.extend({
            get_taxes: function(){

                if (this.order.is_tax_free_order){
                    return [];
                }
                var taxes = _super_order_line.get_taxes.apply(this,arguments);
                return taxes;
            },
            get_applicable_taxes: function(){

                if (this.order.is_tax_free_order){
                    return [];
                }
                var taxes = _super_order_line.get_applicable_taxes.apply(this,arguments);
                return taxes;
            },
            compute_all: function(taxes, price_unit, quantity, currency_rounding, no_map_tax){

                if (this.order.is_tax_free_order){
                    arguments[0] = []
                }
                return _super_order_line.compute_all.apply(this,arguments);
            },
        });

    });
