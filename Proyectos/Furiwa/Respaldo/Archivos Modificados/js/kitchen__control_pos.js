odoo.define('hnet_kitchen_control.kitchen_control',function(require) {
    "use strict";

var models = require('point_of_sale.models');
var screens = require('point_of_sale.screens');
var pedido = require('pos_restaurant.multiprint');
var chrome = require('point_of_sale.chrome');
var gui = require('point_of_sale.gui');
var core = require('web.core');
var QWeb = core.qweb;
var PopupWidget = require('point_of_sale.popups');
var rpc = require('web.rpc');
var _t  = require('web.core')._t;
var session = require('web.session');
models.load_fields('hr.employee', 'is_waiter');
models.load_fields('hr.employee.public', 'is_waiter');

    //Cargar el boton de pedidos listos para facturacion al pos
    /*
    var KitchenOrderButton = screens.ActionButtonWidget.extend({
    template: 'kitchenControlButton',
    button_click: function(){
        var self = this;
        self.custom_function()
    },

    custom_function: function(){
        //var orders = this.pos.sale_orders;
        this.gui.show_screen('KitchenOrdersWidget')
    }
    });
    screens.define_action_button({
        'name':'custom_button',
        'widget': KitchenOrderButton,
        'condition': function(){
        return this.pos.config.mostrar_inputs;
        },
    });
    */

    
    models.load_fields('pos.session', 'correlativo_comanda');
    chrome.OrderSelectorWidget.include({
        renderElement: function(){
            var self = this;
            this._super();

            this.$('.add-Factura').click(function(event){
                self.gui.show_screen('KitchenOrdersWidget');
            });

            this.$('.ver-pedidos').click(function(event){
                self.gui.show_screen('SaleOrdersWidget')
            });
            this.$('.btn-regresar').click(function(event){
                self.gui.show_screen('products')
            });
        },
    });

   // Para cargar la lista de pedidos para facturar!
    var KitchenOrdersWidget = screens.ScreenWidget.extend({
        template: 'KitchenOrdersWidget',

        init: function(parent, options){
            this._super(parent, options);

        },
        auto_back: true,
        show: function(){
            var self = this;
            this._super();
            this.renderElement();
            this.$('.back').click(function(){
                self.gui.back();
            });
            this.render_list();
        },
        click_mostrar_pedido: function(e){
            var order = $(e.target).closest("tr").data('id');
            this.mostrar_pedido(order);
         },
        events: {
        'click .repeat-button.repeat_order': 'click_mostrar_pedido',
        },
        render_list: function(){

             var contents = this.$el[0].querySelector('.show-order-list-lines');
             rpc.query({
                model: 'kitchen.control',
                method: 'get_kitchen_orders',
                }).then(function (result) {

                if (contents){
                    contents.innerHTML = "";

                    for(var i = 0, len = Math.min(result.length,1000); i < len; i++) {
                       if (result[i]) {
                        var order = result[i];
                        var clientline_html = QWeb.render('KitchenShowOrderLines', {widget: this, order: order});
                        var orderline = document.createElement('tbody');

                        orderline.innerHTML = clientline_html;

                        orderline = orderline.childNodes[1];
                        contents.appendChild(orderline);

                       }
                    }

                }
            }).catch(function (e) {
                alert("NO DATA " + e.message)
            });
        },
        mostrar_pedido:function(order_id){
            var self = this;
            self.gui.show_popup('CargarPedidoWidget',{ref: order_id});
        },
    });
    gui.define_screen({name:'KitchenOrdersWidget', widget: KitchenOrdersWidget});


    //Cargar pop up con la info del pedido listo para facturar
    var CargarPedidoWidget = PopupWidget.extend({
    template:'CargarPedidoWidget',

    init: function(parent, options){
        this._super(parent, options);
        this.options = {};
        this.pos_reference = "";
    },
    show: function(options){
        this._super(options);
        this.render_list(options);
    },
    events: {
        'click .button.cancel':  'click_cancel',
        'click .button.confirm': 'click_confirm',
    },
    render_list:function(options){

        $("#table-body").empty();
        var lines = [];
        this.pos_reference = options.ref

        rpc.query({
                model: 'kitchen.control',
                method: 'get_kitchen_orders_lines',
                args: [options.ref],
            }).then(function (result) {
                lines = result[0];
                var sale_order_ref = "<p style= 'display:none;' id='kitchen_order'>"+result[1]+ "</p>"
                $(sale_order_ref).appendTo("#div-tabla");
                var hora_elaboracion = "<p style= 'display:none;' id='hora_elaboracion'>"+result[2]+ "</p>"
                $(hora_elaboracion).appendTo("#div-tabla");

                for(var j=0;j < lines.length; j++){
                    var product_line = lines[j];
                    var rows = "";
                    var id = product_line.product_id
                    var price_unit = product_line.price_unit;
                    var name = product_line.product;
                    var qty = product_line.qty;
                    var line_id = product_line.line_id;
                    var discount = product_line.discount;
                    var client_id = product_line.client_id;
                    rows += "<tr> <td style='display:none;'>" + id + "</td> <td>" + price_unit +" </td> <td>" + name + "</td> <td>" + qty + "</td> <td style='display:none;'>" + discount + "</td> <td style='display:none;'>"+ client_id + "</td></tr>";
                    $(rows).appendTo("#list tbody");
                }

            }).catch(function () {
                alert("NO DATA")
            });

    },
    click_confirm: function(){
        var self = this;
	    var myTable = document.getElementById('list').tBodies[0];
        var order = self.pos.get_order();
        // Cargar id del pedido de cocina
	    self.pos.kitchenOrder = document.getElementById('kitchen_order').innerHTML;
	    document.getElementById('kitchen_order').remove();
	    //Cargar hora de elaboracion
	    order.hora_elaboracion = document.getElementById('hora_elaboracion').innerHTML;
	    order.block_print = true;
	    document.getElementById('hora_elaboracion').remove();

	      for (var r=0, n = myTable.rows.length; r < n; r++) {
            var row = myTable.rows[r]
            var partner = self.pos.db.get_partner_by_id(row.cells[5].innerHTML);
            }

        for (var r=0, n = myTable.rows.length; r < n; r++) {
            var row = myTable.rows[r]
            var product   = this.pos.db.get_product_by_id(row.cells[0].innerHTML);
            if (!product) {
                return;
            }


             this.pos.get_order().add_product(product, {
                price: row.cells[1].innerHTML,
                quantity: row.cells[3].innerHTML,
                discount:row.cells[4].innerHTML,
                merge: false,
                });

            var partner = self.pos.db.get_partner_by_id(row.cells[5].innerHTML);

            this.pos.get_order().set_client(partner);
            if (this.options.client){
                    this.pos.get_order().set_client(self.pos.db.get_partner_by_id(this.options.client));
                }

            }

            this.gui.close_popup();
            this.gui.show_screen('products');

    },
    click_cancel: function(){
        this.gui.close_popup();
    },

});
    gui.define_popup({name:'CargarPedidoWidget', widget: CargarPedidoWidget});

    // Mover el estado del pedido en KO
     screens.PaymentScreenWidget.include({
        validate_order: function(force_validation) {
        if (this.order_is_valid(force_validation)) {
            this.finalize_validation();

            if(this.pos.kitchenOrder !== false && this.pos.kitchenOrder !== undefined ){
                var order_name = this.pos.kitchenOrder;
                var num_factura = this.old_order.name;

                    rpc.query({
                        model: 'kitchen.control',
                        method: 'procesar_pos_Kitchen_order',
                        args: [order_name, num_factura],
                    }).then(function (result) {

                    });
                    this.pos.kitchenOrder = false;
                }

            }
         },
    });

////////////////////////////////////////////////////////////////////////////////////////////
                    /* Cargar las ordenes de venta del E-commerce */
////////////////////////////////////////////////////////////////////////////////////////////


    //Cargar el boton de pedidos de venta al pos
    /*
    var SaleOrderButton = screens.ActionButtonWidget.extend({
    template: 'SalesOrderButton',
    button_click: function(){
        var self = this;
        self.custom_function()
    },

    custom_function: function(){
        var orders = this.pos.sale_orders;
        this.gui.show_screen('SaleOrdersWidget')
    }
    });
    screens.define_action_button({
        'name':'custom_button',
        'widget': SaleOrderButton,
        'condition': function(){
        return this.pos.config.mostrar_inputs;
        },
    });
    */

   // Para cargar la lista de ordenes!
    var SaleOrdersWidget = screens.ScreenWidget.extend({
        template: 'SaleOrdersWidget',

        init: function(parent, options){
            this._super(parent, options);
            this.order_string ="";
        },
        auto_back: true,
        get_sale_orders_data: function(){
            var self = this;
            return this._rpc({
            model: "sale.order",
            method: 'get_sale_orders',
        }).then(function (result) {
            self.sale_orders_data = result;
         });
        },
        show: function(){
            var self = this;
            this._super();
            this.renderElement();
            this.$('.back').click(function(){
                self.gui.back();
            });
            var sale_orders = this.pos.sale_orders;
            this.render_list(sale_orders);
        },
        click_mostrar_pedido: function(e){
            var order = $(e.target).closest("tr").data('id');
            this.mostrar_pedido(order);
         },
        events: {
            'click .repeat-button.repeat_order': 'click_mostrar_pedido',
        },
        render_list: function(sale_orders){

            var self = this;

             var contents = this.$el[0].querySelector('.show-order-list-lines');
             rpc.query({
                model: 'sale.order',
                method: 'get_sale_orders',
                }).then(function (result) {

                if (contents){
                    contents.innerHTML = "";

                    for(var i = 0, len = Math.min(result.length,1000); i < len; i++) {
                       if (result[i]) {
                        var order = result[i];
                        var clientline_html = QWeb.render('ShowOrderLines', {widget: this, order: order});
                        var orderline = document.createElement('tbody');
                        orderline.innerHTML = clientline_html;
                        orderline = orderline.childNodes[1];
                        contents.appendChild(orderline);
                       }
                    }

                }
            }).catch(function (e) {
                alert("NO DATA " + e.message)
            });
        },
        mostrar_pedido:function(order_id){
            var self = this;
            self.gui.show_popup('MostrarPedidoWidget',{ref: order_id});
        },
    });

    gui.define_screen({name:'SaleOrdersWidget', widget: SaleOrdersWidget});

    //Cargar pop up con la info del pedido
    var MostrarPedidoWidget = PopupWidget.extend({
    template:'MostrarPedidoWidget',

    init: function(parent, options){
        this._super(parent, options);
        this.options = {};
        this.pos_reference = "";

    },
    show: function(options){
        this._super(options);
        this.render_list(options);
    },
    events: {
        'click .button.cancel':  'click_cancel',
        'click .button.confirm': 'click_confirm',
    },
    render_list:function(options){
        $("#table-body").empty();
        var lines = [];

        rpc.query({
                model: 'sale.order',
                method: 'get_sale_orders_lines',
                args: [options.ref],
            }).then(function (result) {
                lines = result[0];
                var sale_order_ref = "<p id='sale_order'>"+ result[1].name + "</p>"
                var ref = "<p id='ref' style='display:none;'>"+ result[1].ref + "</p>"
                var proveniente = "<p id='proveniente' style='display:none;'>"+ result[1].proveniente + "</p>"

                $(sale_order_ref).appendTo("#list");
                $(ref).appendTo("#list");
                $(proveniente).appendTo("#list");
                for(var j=0;j < lines.length; j++){
                    var product_line = lines[j];
                    var rows = "";
                    var id = product_line.product_id
                    var price_unit = product_line.price_unit;
                    var name = product_line.product;
                    var qty = product_line.qty;
                    var line_id = product_line.line_id;
                    var discount = product_line.discount;
                    var client_id = product_line.client_id;
                    var note = product_line.note;

                    rows += "<tr> <td style='display:none;'>" + id + "</td> <td>" + price_unit +" </td> <td>" + name + "</td> <td>" + qty + "</td> <td style='display:none;'>" + discount + "</td> <td style='display:none;'>"+ client_id + "</td>" + "<td style='display:none;'>"+ note + "</td></tr>";
                    $(rows).appendTo("#list tbody");
                }

            }).catch(function () {
                alert("NO DATA")
            });
    },
    click_confirm: function(){
        var self = this;
	    var myTable = document.getElementById('list').tBodies[0];

        this.pos.miOrden = false

        //sale order
	    self.pos.miOrden = document.getElementById('sale_order').innerHTML;
	    document.getElementById('sale_order').remove();

	    //ref
	    self.pos.ref_pedido = document.getElementById('ref').innerHTML;
	    document.getElementById('ref').remove();

	    //proveniente
	    self.pos.proveniente = document.getElementById('proveniente').innerHTML;
	    document.getElementById('proveniente').remove();

	    var notes_json = {}

        for (var r=0, n = myTable.rows.length; r < n; r++) {
            var row = myTable.rows[r]
            var product   = this.pos.db.get_product_by_id(row.cells[0].innerHTML);
            if (!product) {
                return;
            }
             this.pos.get_order().add_product(product, {
                price: row.cells[1].innerHTML,
                quantity: row.cells[3].innerHTML,
                discount:row.cells[4].innerHTML,
                note:row.cells[5].innerHTML,
                merge: false,
                });

            notes_json[row.cells[0].innerHTML] = row.cells[6].innerHTML
            var partner = self.pos.db.get_partner_by_id(row.cells[5].innerHTML);

            if (partner){
                this.pos.get_order().set_client(partner);
                if (this.options.client){
                    this.pos.get_order().set_client(self.pos.db.get_partner_by_id(this.options.client));
                }
            }
            else{
                this.recargar_clientes(row.cells[5].innerHTML);
            }
        }

            var order = this.pos.get_order()
            order.get_orderlines().forEach(function (orderline) {
                for(var i in notes_json ){
                    if( orderline.product.id == i){
                        if(notes_json[i] != "false"){
                            orderline.set_note(notes_json[i])
                        }

                    }
                }
            });

            this.gui.close_popup();
            this.gui.show_screen('products');
    },
    click_cancel: function(){
        this.gui.close_popup();
    },
    recargar_clientes: function(id){
        var self = this;
        return this.pos.load_new_partners().then(function(){
            // partners may have changed in the backend
                self.partner_cache = new screens.DomCache();
            var partner_id = self.pos.db.get_partner_by_id(id);

            if(id){
                var partner = self.pos.db.get_partner_by_id(id);
                self.pos.get_order().set_client(partner);
            }
        });
    },

});

gui.define_popup({name:'MostrarPedidoWidget', widget: MostrarPedidoWidget});

// ------------------------------------------------------------------------------------------------------------------ //
// Bloquear botón de Notas y cantidades cuando el pedido se mande a cocina
screens.OrderWidget.include({
    // Sobre escribir el renderizado de las orderlines
    render_orderline: function(orderline){

        var el_str  = QWeb.render('Orderline',{widget:this, line:orderline});
        var el_node = document.createElement('div');
            el_node.innerHTML = _.str.trim(el_str);
            el_node = el_node.childNodes[0];
            el_node.orderline = orderline;
            el_node.addEventListener('click',this.line_click_handler);
        var el_lot_icon = el_node.querySelector('.line-lot-icon');
        if(el_lot_icon){
            el_lot_icon.addEventListener('click', (function() {
                this.show_product_lot(orderline);
            }.bind(this)));
        }

        orderline.node = el_node;

        // Obtener el cajero y el botón notas en sus distintos estados
        var cashier = this.pos.get('cashier') || this.pos.get_cashier();
        var elem_note = $('[class="control-button note"]');
        var block_note = $('[class="control-button note disabled"]');

        if(orderline.length != 0){

            // Obtener la categoria de a la que pertenecen el producto de la orderline
            var categ_id = orderline.product.categ_id[1];
            var food_cat = categ_id.split('/');

            // Obtener los botones cantidad, eliminar y en distintos estados
            var qty_button = $('.mode-button[data-mode="quantity"]');
            var delete_button = $('[class="input-button numpad-backspace"]')
            var selected_button = $('[class="selected-mode mode-button"]');

            // Obtener el html del botón cantidad y el seleccionado para compararlos
            var qty_html = $(qty_button).html();
            var selected_html = $(selected_button).html();

            if(food_cat[0] == 'Furiwa ' || food_cat[0] == 'Tokyo '){

                // Obtener los botones sentinela en estado necesario para bloquear los botones
                var to_kitchen = $('[class="control-button order-submit highlight"]');
                var note_state = $('#note_tokitchen');

                if(to_kitchen.length == 0 || note_state.length != 0){
                    if(cashier.role == "cashier"){

                        // Bloqueo de botones si es cajero o mesero
                        if(qty_html == selected_html){
                            $(qty_button).removeClass('selected-mode mode-button');
                            $(qty_button).addClass('mode-button disabled-mode');
                        }
                        $(elem_note).addClass('disabled');
                        $(elem_note).css("pointer-events","none");
                        $(qty_button).prop('disabled', true);
                        $(delete_button).css("pointer-events","none");;
                    }else{
                        $(block_note).removeClass('disabled');
                        $(block_note).css("pointer-events","auto");
                        $(qty_button).removeProp('disabled');
                        $(delete_button).css("pointer-events","auto");
                    }
                    $(note_state).removeAttr('id');
                }else{
                    // Desbloqueo de botones si es administrador
                    $(qty_button).removeClass('mode-button disabled-mode');
                    $(qty_button).addClass('selected-mode mode-button');
                    $(block_note).removeClass('disabled');
                    $(block_note).css("pointer-events","auto");
                    $(qty_button).removeProp('disabled');
                    $(delete_button).css("pointer-events","auto");
                }
            }else{
                // Desbloqueo de botones si la categoria no corresponde a las que necesitan comanda
                $(qty_button).removeClass('mode-button disabled-mode');
                $(qty_button).addClass('selected-mode mode-button');
                $(block_note).removeClass('disabled');
                $(block_note).css("pointer-events","auto");
                $(qty_button).removeProp('disabled');
                $(delete_button).css("pointer-events","auto");
            }
        }
        return el_node;
    },
});
// ------------------------------------------------------------------------------------------------------------------ //
    // Botón "Pedir" para crear el pedido de cocina
    // Cargar al boton de mandar a imprimir a comanda de cocina 
    pedido.SubmitOrderButton.include({
    query_pedidos: function (modelo, nombre_funcion,args_func){

      rpc.query({
                model: modelo,
                method: nombre_funcion,
                args: args_func,
            });

    },
    update_correlativo_comanda: function (session_id, value){
      rpc.query({
                model: 'pos.session',
                method: 'actualizar_correlativo_comanda',
                args: [session_id, value],
            });
    },
    button_click: async function(){

        var order = this.pos.get_order();
        var note_button = $('[class="control-button note"]');
        $(note_button).attr('id', 'note_tokitchen');

        if(order.hasChangesToPrint()){

            let session =  this.pos.pos_session
            let num_comanda_actual = session.correlativo_comanda
            let siguiente_numero = num_comanda_actual + 1
            this.pos.pos_session.correlativo_comanda = siguiente_numero
            //mandar a guardar el numero del recibo
            this.update_correlativo_comanda(session.id, siguiente_numero)
            await order.printChanges();
            order.block_delete = true;
            order.proveniente = false;
            order.ref_pedido = false;
            order.saveChanges();

            let orderlines = order.orderlines.models;
            var notes ={};

            // Obtener notas del pedido
            for(var i=0; i < orderlines.length; i++){
                var note = orderlines[i].note
                var product_id = orderlines[i].product.id;
                if(product_id in notes){
                    notes[product_id] = notes[product_id]+ ", " + note;
                }else{
                    notes[product_id] = note;
                }
            }
            let self = this;
            var ref = false;

            var date = new Date();
                var hora_array = date.toLocaleString().split(" ");
                self.hora = hora_array[1];
                self.hora = hora_array[2] ? self.hora + " " +  hora_array[2] : self.hora ;

            //Mandar a crear el pedido a cocina!
            var current_table = this.pos.table['name'];

            if(current_table == 'Delivery' || current_table == 'delivery' || current_table == 'Deliveries' || current_table == 'deliveries'){
                /*
                var _team = this.pos.delivery_filter;
                if(_team != undefined){
                    this.query_pedidos('pos_pedidos_cocina','create_pedido_cocina', [_team, 'delivery',self.hora]);
                }
                */
                
    
            }
            /* ----------------------------- Ya no se necesita -----------------------------
            if(this.pos.miOrden !== false && this.pos.miOrden !== false){
                var order_name = this.pos.miOrden;

                rpc.query({
                        model: 'kitchen.control',
                        method: 'create_kitchen_order',
                        args: [order_name, notes],
                    }).then( function (kitchen) {
                        console.log(kitchen);
                        if(kitchen[2]){
                            
                            console.log(kitchen[2]);


                          self.query_pedidos('pos_pedidos_cocina','create_pedido_cocina', [kitchen[2], 'delivery', self.hora, ])
                        }
                        alert(kitchen[1])
                    });
                self.pos.delete_current_order()
                self.pos.miOrden = false;
                self.pos.proveniente = true;
                self.pos.ref_pedido = true;
            }else{
                ref = this.pos.table.name;
                this.query_pedidos('pos_pedidos_cocina','create_pedido_cocina', [ref, 'mesa',self.hora])
            }
            */
        }
    },
});

});