odoo.define('hnet_kitchen_control.btn_pedidos_cocina',function(require) {
    "use strict";

    var chrome = require('point_of_sale.chrome');
    var models = require('point_of_sale.models');
    var pos = require('point_of_sale.screens');
    var gui = require('point_of_sale.gui');
    var screens = require('point_of_sale.screens');
    var rpc = require('web.rpc');
    var core = require('web.core');
    var _t  = require('web.core')._t;
    var PopupWidget = require('point_of_sale.popups');
    var QWeb = core.qweb;

    // Cargar equipos de ventas al POS
    models.load_models([{
        model:  'crm.team',
        fields: ['name'],
        domain: function(self){ return [['cargar_pos', '=', true]]; },
        loaded: function(self, equipo_ventas) {
            self.equipo_ventas = equipo_ventas;
        }
    }]);

    // Cargar accion al boton de pedidos en cocina
    pos.ProductScreenWidget.include({
        renderElement: function(){
            var self = this;
            this._super();
            var btn = this.$('.show-pedidos');
            this.$('.show-pedidos').click(function(event){
                self.gui.show_screen('KitchenWidget');
            });
        },

    });

    // Para cargar la lista de pedidos en Cocina
    var KitchenWidget = screens.ScreenWidget.extend({
        template: 'KitchenWidget',

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

            // FILTRO
            if(this.pos.delivery_filter){
                this.render_list(this.pos.delivery_filter);
            }else{
                this.render_list();
            }

        },
        click_cocina: function(e){
            $('.cocina-filter').addClass('highlight');
            $('.facturacion-filter').removeClass('highlight');
            $('.despachado-filter').removeClass('highlight');
            this.render_list("cocina");
        },
        click_facturacion: function(e){
            $('.cocina-filter').removeClass('highlight');
            $('.facturacion-filter').addClass('highlight');
            $('.despachado-filter').removeClass('highlight');
            this.render_list("facturacion");
        },
        click_despachado: function(e){
            $('.cocina-filter').removeClass('highlight');
            $('.facturacion-filter').removeClass('highlight');
            $('.despachado-filter').addClass('highlight');
            this.render_list("despachado");
        },
        click_mostrar_pedido: function(e){
            var order = $(e.target).closest("tr").data('id');
            this.mostrar_pedido(order);
         },
        events: {
            'click .cocina-filter': 'click_cocina',
            'click .facturacion-filter': 'click_facturacion',
            'click .despachado-filter': 'click_despachado',
            'click .repeat-button.repeat_order': 'click_mostrar_pedido',
        },
        mostrar_pedido:function(order_id){
            var self = this;
            self.gui.show_popup('CargarPedidoWidget',{ref: order_id});
        },
        render_list: function(filtro){

             var contents = this.$el[0].querySelector('.show-order-list-lines');
             var header = this.$el[0].querySelector('#titulo-filtro');
             var filter = filtro ? filtro : false;
             var equipo = this.pos.equipo_ventas;
             rpc.query({
                model: 'pos_pedidos_cocina',
                method: 'get_pedidos_cocina',
                args:[filter],
                }).then(function (result) {
                if (contents){
                    contents.innerHTML = "";
                    header.innerHTML = filter ? filter : ""

                    /*
                    if(filter){
                        for(var delivery_id in equipo){
                            if(equipo[delivery_id].id == filter){
                            header.innerHTML = "Delivery"
                            }
                        }
                    }
                    */

                    for(var i = 0, len = Math.min(result.length,1000); i < len; i++) {
                       if (result[i].referencia) {
                        var order = result[i];
                        var clientline_html = QWeb.render('KitchenOrderLines', {widget: this, ref: order});
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
            // this.pos.delivery_filter = false;
        },
    });
    gui.define_screen({name:'KitchenWidget', widget: KitchenWidget});

    // Popup con los equipos de ventas
     var PopupDeliveriesWidget = PopupWidget.extend({
        template:'PopupDeliveriesWidget',

        init: function(parent, options){
            this._super(parent, options);
        },
        show: function(options){
            this._super(options);
            this.list();
        },
        list: function(){
            var self = this;
            var contents = this.$el[0].querySelector('#tabla-deliveries');

            var equipo_ventas = this.pos.equipo_ventas ? this.pos.equipo_ventas : []
              if (contents){
                contents.innerHTML = "";

                for(var i = 0, len = Math.min(equipo_ventas.length,1000); i < len; i++) {
                   if (equipo_ventas[i]) {
                    var team_name= equipo_ventas[i];
                    var clientline_html = QWeb.render('PopupDeliveriesLinesWidget', {widget: this, team_name: team_name});
                    var orderline = document.createElement('tbody');
                    orderline.innerHTML = clientline_html;
                    orderline = orderline.childNodes[1];
                    contents.appendChild(orderline);
                   }
                }
            }
        },
        events: {
            'click .button.cancel':  'click_cancel',  // Cancelar
            'click .button.confirm':  'click_confirm',   // Cliente
            'click .control-button.delivery': 'deliveries',   // Click en algun equipo de ventas
        },
        click_cancel: function(){
            if(this.pos.get_order()){
                var screen = this.pos.get_order().get_screen_data('screen');
                if(screen == 'products'){
                    $('.floor-button').click();
                }
            }
        },
        click_confirm: function(){
            this.gui.show_screen('clientlist');
        },
        deliveries: function(e){

            // id del equipo de ventas
            var filter = e.target.id;

            // Equipo de ventas
            var team_sales = this.pos.equipo_ventas ? this.pos.equipo_ventas : []
            var team_selected;

            // Clientes
            var customers = this.pos.db.get_partners_sorted(1000);

            // Cliente seleccionado
            var curr_client = this.pos.get_order().get_client();
            var verify_client = false;

            for (var i = 0; i < customers.length ; i++){
                var client_name = customers[i].name;
                for (var j = 0; j < team_sales.length; j++){
                    if(team_sales[j].id == filter){
                        var team_name = team_sales[j].name;
                        if(client_name == team_name){
                            // Cliente predeterminado de equipo de ventas encontrado
                            verify_client = true;
                            this.pos.get_order().set_client(this.pos.db.get_partner_by_id(customers[i].id));
                            team_selected = team_sales[j].name;
                        }
                    }
                }
            }

            if(curr_client){
                verify_client = true;
            }

            // Establecer cliente para los equipos de ventas que no tienen cliente predeterminado
            if(verify_client == false && !curr_client){
                alert(_t("Debe establecer un cliente primero"));
                this.gui.show_screen('clientlist');
            }else{
                this.pos.delivery_filter = team_selected;
                this.gui.show_screen('products');
            }
        }
     });
    gui.define_popup({name:'PopupDeliveriesWidget', widget: PopupDeliveriesWidget});

    // Popup con los productos del pedido 
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
                    var _team = this.pos.delivery_filter;
                    if(_team != undefined){
                        this.query_pedidos('pos_pedidos_cocina','create_pedido_cocina', [_team, 'delivery',self.hora]);
                    }
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
