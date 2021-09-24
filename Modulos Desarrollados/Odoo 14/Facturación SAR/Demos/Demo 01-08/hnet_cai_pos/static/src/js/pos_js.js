/*
    @author ebenedetto@hnetw.com - HNET
    @date 26/07/2021
    @decription Calculo de impuestos, bases y exonerado
    @name_file pos_js.js
    @version 1.0
*/

odoo.define('pos_dei.pos_dei', function(require){
'use strict';

    var models = require('point_of_sale.models');
    var core = require('web.core');
    var utils = require('web.utils');
    var QWeb = core.qweb;
    var _t = core._t;
    var round_di = utils.round_decimals;
    var round_pr = utils.round_precision;

    const { gui } = require('point_of_sale.Gui');
    const PosComponent = require('point_of_sale.PosComponent');
    const { posbus } = require('point_of_sale.utils');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');
    const PaymentScreen = require('point_of_sale.PaymentScreen');


    var OrderlineSuper = models.Orderline;
    models.Orderline = models.Orderline.extend({
    compute_all1: function(taxes, price_unit, quantity, currency_rounding, no_map_tax) {
        var self = this;
        var list_taxes = [];
        var currency_rounding_bak = currency_rounding;
        if (this.pos.company.tax_calculation_rounding_method == "round_globally"){
           currency_rounding = currency_rounding * 0.00001;
        }
        var total_excluded = round_pr(price_unit * quantity, currency_rounding);
        var total_included = total_excluded;
        var base = total_excluded;

        _(taxes).each(function(tax) {
            if (!no_map_tax){
                tax = self._map_tax_fiscal_position(tax);
            }
            if (!tax){
                return;
            }
            if (tax.amount_type === 'group'){
                var ret = self.compute_all(tax.children_tax_ids, price_unit, quantity, currency_rounding);
                total_excluded = ret.total_excluded;
                base = ret.total_excluded;
                total_included = ret.total_included;
                list_taxes = list_taxes.concat(ret.taxes);
            }
            else {
                var tax_amount = self._compute_all(tax, base, quantity);
                tax_amount = round_pr(tax_amount, currency_rounding);

                if (tax_amount){
                    if (tax.price_include) {
                        total_excluded -= tax_amount;
                        base -= tax_amount;
                    }
                    else {
                        total_included += tax_amount;
                    }
                    if (tax.include_base_amount) {
                        base += tax_amount;
                    }
                    var data = {
                        id: tax.id,
                        amount: tax_amount,
                        name: tax.name,
                    };
                    list_taxes.push(data);
                }
            }

        });
        return {
            taxes: list_taxes,
            total_excluded: round_pr(total_excluded, currency_rounding_bak),
            total_included: round_pr(total_included, currency_rounding_bak)
        };
    },

    get_all_prices1: function(){
        var price_unit = this.get_unit_price() * (1.0 - (this.get_discount() / 100.0));
        var taxtotal = 0;

        var product =  this.get_product();
        var taxes_ids = product.taxes_id;
        var taxes =  this.pos.taxes;
        var taxdetail = {};
        var product_taxes = [];

        _(taxes_ids).each(function(el){
            product_taxes.push(_.detect(taxes, function(t){
                if(t.name == "15% ISV" && t.id === el){
                    //console.log("Testing>>>>>>>>>>>2222222>>>>>>>>>>>>",t);

                    return true;
                }

                return false;
            }));
        });
        if(product_taxes.length > 0 && product_taxes[0] != undefined){
            // console.log("Testing>>>>>>>>rRRRRRR>>>>>>>>>>>>>>>",product_taxes);
            var all_taxes = this.compute_all1(product_taxes, price_unit, this.get_quantity(), this.pos.currency.rounding);
            // console.log("Testing>>>>>>>>All taxes>>>>>>>>>>>>>>>",all_taxes);
            return {
                "priceWithoutTax": all_taxes.total_excluded,
            };
        }
        else{
            return {
                "priceWithoutTax": 0,

            };

        }

    },
    get_all_prices2: function(){
        var price_unit = this.get_unit_price() * (1.0 - (this.get_discount() / 100.0));
        var taxtotal = 0;

        var product =  this.get_product();
        var taxes_ids = product.taxes_id;
        var taxes =  this.pos.taxes;
        var taxdetail = {};
        var product_taxes = [];

        _(taxes_ids).each(function(el){
            product_taxes.push(_.detect(taxes, function(t){
                if(t.name == "18% ISV" && t.id === el){
                    // console.log("Testing>>>>>>>>>>>2222222>>>>>>>>>>>>",t);
                    return true;
                }
                return false;
            }));
        });
        if(product_taxes.length > 0 && product_taxes[0] != undefined){
            // console.log("Testing>>>>>>>>rRRRRRR>>>>>>>>>>>>>>>",product_taxes);
            var all_taxes = this.compute_all1(product_taxes, price_unit, this.get_quantity(), this.pos.currency.rounding);
            // console.log("Testing>>>>>>>>All taxes>>>>>>>>>>>>>>>",all_taxes);
            return {
                "priceWithoutTax": all_taxes.total_excluded,
            };
        }
        else{
            return {
                "priceWithoutTax": 0,
            };

        }
    },
    get_all_prices3: function(){
        var price_unit = this.get_unit_price() * (1.0 - (this.get_discount() / 100.0));
        var taxtotal = 0;

        var product =  this.get_product();
        var taxes_ids = product.taxes_id;
        var taxes =  this.pos.taxes;
        var taxdetail = {};
        var product_taxes = [];

        _(taxes_ids).each(function(el){
            product_taxes.push(_.detect(taxes, function(t){
                if(t.name == "15% ISV" || t.name == "18% ISV"){
                    return false;
                }
                else if(t.id === el){
                    return true;
                }

            }));
        });
        // console.log("Testing>>>>>>>>rRRRRRR>3333>>>>>>>>>>>>>>",product_taxes);
        if(product_taxes.length == 0){
            var all_taxes = this.compute_all1(product_taxes, price_unit, this.get_quantity(), this.pos.currency.rounding);
            // console.log("Testing>>>>>>>>All taxes>>33333>>>>>>>>>>>>>",all_taxes);
            return {
                "priceWithoutTax": all_taxes.total_excluded,
            };
        }
        else{
            return {
                "priceWithoutTax": 0,

            };

        }
    },

        get_price_without_tax1: function(){
            return this.get_all_prices1().priceWithoutTax;
        },
        get_price_without_tax2: function(){
            return this.get_all_prices2().priceWithoutTax;
        },
        get_price_without_tax3: function(){
            return this.get_all_prices3().priceWithoutTax;
        },

    });
    var OrderSuper = models.Order;
    models.Order = models.Order.extend({
        /* Overload Section */

        get_tax_details_all: function(){
            var tax_details = this.get_tax_details();
            var get_tax_details_15 = 0.0;
            var get_tax_details_18 = 0.0;
            for(var i=0;i<tax_details.length;i++){
                if(tax_details[i].name == "15% ISV"){
                    get_tax_details_15 = tax_details[i].amount;
                }
                if(tax_details[i].name == "18% ISV"){
                    get_tax_details_18 = tax_details[i].amount;
                }
            }

            return {
                tax15 : get_tax_details_15,
                tax18 : get_tax_details_18

            };
        },

        get_tax_15: function() {
            return round_pr((this.get_orderlines()).reduce((function(sum, orderLine) {
                return sum + orderLine.get_price_without_tax1();
            }), 0), this.pos.currency.rounding);
        },
        get_tax_18: function() {
            return round_pr((this.get_orderlines()).reduce((function(sum, orderLine) {

                return sum + orderLine.get_price_without_tax2();
            }), 0), this.pos.currency.rounding);
        },
        get_tax_simple: function() {

            return round_pr((this.get_orderlines()).reduce((function(sum, orderLine) {
                return sum + orderLine.get_price_without_tax3();
            }), 0), this.pos.currency.rounding);
        },
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
        add_discount_ex: function(){
            this.pos.get_order().clean_empty_paymentlines();
            var order = this.pos.get_order();
            if(order.note1.length ||order.note2.length || order.note3.length){
                order.is_tax_free_order = false;
                var ext = 0;
                var orderlines = order.get_orderlines();
                $.each(orderlines,function(index){
                    var line = orderlines[index];
                    line.price = line.product.lst_price;
                    ext += line.get_tax();
                    line.price = (line.get_price_without_tax())/line.quantity;
                    line.trigger('change',line);
                });
                order.exento = ext;
                order.is_tax_free_order = true;
                return round_pr(ext,this.pos.currency.rounding);
            }else{
                order.is_tax_free_order=false;
                return false;
            }
        },
        get_ex_amount: function(){
            this.pos.get_order().clean_empty_paymentlines();
            var order = this.pos.get_order();
            if(order.note1.length ||order.note2.length || order.note3.length){
                var price_ext = 0;
                var orderlines = order.get_orderlines();
                $.each(orderlines,function(index){
                    var line = orderlines[index];
                    price_ext += line.get_price_without_tax();
                });
                return round_pr(price_ext,this.pos.currency.rounding);
            }else{
                return false;
            }
        }
    });
});

