odoo.define('pos_2x1.mix_and_match',function(require) {
    "use strict";

    var core = require('web.core');
    var screens = require('point_of_sale.screens');
    var gui = require('point_of_sale.gui');
    var chrome = require('point_of_sale.chrome');
    var models = require('point_of_sale.models');
    var rpc = require('web.rpc');
    models.load_fields('product.product', 'is_sushi');


    var Button_2x1 = screens.ActionButtonWidget.extend({
        template: 'Button_2x1',

        button_click: function(){

            //this.add_sushi_2x1();
            var self = this;
            this._super();
            //get order
            var order = self.pos.get_order();
            //get orderlines
            var orderlines = order.orderlines.models;
            // modify order
            var separate = self.separate_orderlines(self, orderlines, order);
            //if order is
            if(separate){
                self.order_ol(self, orderlines, order);
            }
        },
        // Separate qty to orderlines
        separate_orderlines: function(self, orderlines, order){

            var lines = false;
            orderlines.forEach(line =>{
                var product = line.product;
                var prod = self.pos.db.get_product_by_id(product.id)
                if(product.is_sushi){
                    lines = true;
                    var qty = line.quantity;
                    if(qty > 1){
                        for(var i = 1; i < qty; i++ ){
                            order.add_product(prod, {
                            price: prod.lst_price,
                            quantity: 1,
                            merge: false,
                            });
                        }
                        line.set_quantity(1);
                    }
                }
            });
            return lines
        },
        order_ol: function(self, lines, order){
            let list = [];

            //get lines that care sushi
            lines.forEach(line =>{
                var product = line.product;
                if(product.is_sushi){
                    list.push(line);
                }
            });
            // sort high to low
            const sr = list.sort((a, b) => (a.product.lst_price < b.product.lst_price) ? 1 : -1);

            //Get mid for applying discount
            let mid = Math.floor(sr.length / 2);

            //Para hacer parejas
            let last = sr.length - 1;

            //Apply discount
            for(var i = 0 ; i < mid ;i++ ){
                var order_line = order.get_orderline(sr[last].id);
                order_line.set_discount(100);
                last --;
            }
        }
    });

    screens.define_action_button({
        'name': 'Button_2x1',
        'widget': Button_2x1,
    });
});
