## Odoo 13 - Proyecto Furiwa
### Edgar Josué Benedetto Godoy
### 0801-1997-23600
#### ebenedetto@hnetw.com
#### edgar.benedetto@unah.hn
#### +504 3330-0171
#### 15/07/2021 - 21/07/2021
___
___
# Secuencia de cambios realizados
___

### Recomendaciones

0.  | Usuario | Contraseña | 
    |:-------:|:----------:|
    |admin    | HNET2020** |

1. Devolverle al usuario admin el pin: 44003211997
2. El rango de facturación estaba con la fecha 28/02/2021
3. Agregar a las dependencias ```netifaces==0.11.0```

## Cambios estéticos
1. Cambiar el nombre del botón "Historial" a "Historial pagado" código encontrado en la ruta ``` odoo-custom-addons>pos_orders_history>static>src>xml>pos.xml```

``` html
<t t-name="OrdersHistoryButton">
    <div class='control-button orders-history'>
        <i class='fa fa-list-alt '/> History
    </div>
</t>
```

* Solución Desarrollada en la ruta ```odoo-custom-addons>pos_orders_history>static>src>xml>pos.xml```

``` html
<t t-name="OrdersHistoryButton">
    <div class='control-button orders-history'>
        <i class='fa fa-list-alt '/> Historial Pagado
    </div>
</t>
```

2. Cambiar "Seleccionar cajero" por "Seleccionar Personal" código encontrado en la ruta ``` odoo>addons>pos_hr>static>src>xml```

```html
<span class="login-element">
    <button class="login-button select-employee">Seleccionar Personal</button>
</span>
```


* Solución Desarrollada en la ruta ``` odoo-custom-addons>pos_orders_historyhnet_kitchen_control>static>src>xml>inherit_btn_select_employee.xml```

```html
<?xml version="1.0" encoding="UTF-8"?>
<template xml:space="preserve">
    <t t-extend="LoginScreenWidget">
        <t t-jquery=".login-body" t-operation="replace">
            <div class="login-body">
                <span class="login-element">
                    <img class="login-barcode-img" src="/point_of_sale/static/img/barcode.png"/>
                    <div class="login-barcode-text">Scan your badge</div>
                </span>
                <span class="login-or">or</span>
                <span class="login-element">
                    <button class="login-button select-employee">Seleccionar Personal</button>
                </span>
            </div>
        </t>
    </t>
</template>
```
  

3. Cambiar el nombre del botón "Reimprimir recibo" a "Reimprimir Prefactura" código encontrado en la ruta ``` odoo>addons>pos_reprint>static>src>xml>reprint.xml```

```html
<t t-name="ReprintButton">
    <div class='control-button js_reprint'>
        <i class="fa fa-retweet"></i> Reimprimir Prefactura
    </div>
</t>
```
* Solución Desarrollada en la ruta ``` odoo-custom-addons>pos_orders_historyhnet_kitchen_control>static>src>xml>inherit_btn_select_employee.xml```
```html
<?xml version="1.0" encoding="UTF-8"?>
  <template xml:space="preserve">
      <t t-extend="ReprintButton">
      <t t-jquery=".js_reprint" t-operation="replace">
         <div class='control-button js_reprint'>
             <i class="fa fa-retweet"></i> Reimprimir Prefactura
        </div>
      </t>
    </t>
  </template>
```

4. Cambiar el nombre del Botón "Abarán" a "Cambio de Mesa" código encontrado en la ruta ``` odoo>addons>pos_restaurant>static>src>xml>floors.xml``` 

```html
<t t-name="TransferOrderButton">
    <div class='control-button'>
        <i class='fa fa-arrow-right' /> Transfer 
    </div>
</t>
```

* Solución Desarrollada en la ruta ``` odoo-custom-addons>hnet_kitchen_control>static>src>xml>inherit_btn_transfer.xml```

```html
<?xml version="1.0" encoding="UTF-8"?>
<template xml:space="preserve">
    <t t-extend="TransferOrderButton">
        <t t-jquery=".control-button" t-operation="replace">
         <div class='control-button'>
            <i class='fa fa-arrow-right' /> Cambio de Mesa
        </div>
      </t>
    </t>
</template>
```

5. Cambiar el nombre del botón "Cuenta" a "Aplicar Propina" código encontrado en la ruta ``` odoo>addons>pos_restaurant>static>src>xml>printbill.xml``` 

```html
<t t-name="PrintBillButton">
    <span class="control-button order-printbill">
        <i class="fa fa-print"></i>
        Bill
    </span>
</t>
```

* Solución Desarrollada en la ruta ``` odoo-custom-addons>hnet_kitchen_control>static>src>xml>inherit_btn_bill.xml```

```html
<?xml version="1.0" encoding="UTF-8"?>
<template xml:space="preserve">
    <t t-extend="PrintBillButton">
        <t t-jquery=".order-printbill" t-operation="replace">
        <span class="control-button order-printbill">
            <i class="fa fa-print"></i>
            Aplicar Propina
        </span>
      </t>
    </t>
</template>
```

6. Ocultar botón de reimpresión de última factura cobrada código encontrado en la ruta ``` odoo>addons>pos_reprint>static>src>xml>reprint.xml``` 

```html
<t t-name="ReprintButton">
    <div class='control-button js_reprint'>chrome.OrderSelectorWidget.include({
        renderElement: function(){
        <i class="fa fa-retweet"></i> Reprint Receipt
    </div>
</t>
```

* Solución Desarrollada en la ruta ``` odoo-custom-addons>hnet_kitchen_control>static>src>xml>inherit_btn_reprint_bill.xml```
    
```html
<?xml version="1.0" encoding="UTF-8"?>
<template xml:space="preserve">
    <t t-extend="ReprintButton">
        <t t-jquery=".js_reprint" t-operation="replace">
            <div class='control-button js_reprint' style="display:none">
            <i class="fa fa-retweet"></i> Reprint Receipt
        </div>
      </t>
    </t>
</template>
```

7. Agregar una “mesa” dentro del POS que se llame menú. Solamente servirá para entrar y consultar productos, no para creación de pedidos. Al momento de entrar a esta mesa se deben bloquear los botones para que no pueda realizar ninguna acción 

* Solución Desarrollada en la ruta ``` odoo-custom-addons>hnet_kitchen_control>static>src>js>menu_hide_buttons.js```

```js
odoo.define('hnet_kitchen_control.menu_hide_buttons',function(require) {
    "use strict";

    var screens = require('point_of_sale.screens');
    var models = require('point_of_sale.models');
    models.load_fields('hr.employee', 'is_waiter');
    models.load_fields('hr.employee.public', 'is_waiter');

    // Ocultar botones para la mesa llamada menú
    screens.ScreenWidget.include({
        show: function(){
            this._super();
            if(this.pos.table != null){
                var current_table = this.pos.table['name'];

                if(current_table == 'Menú'){
                    this.$('.control-buttons').addClass('oe_hidden');
                    this.$('.actionpad').addClass('oe_hidden');
                }else{
                    this.$('.control-buttons').removeClass('oe_hidden');
                    this.$('.actionpad').removeClass('oe_hidden');
                }
            }
        }
    });
});
```
8. Los pedidos de eCommerce cambiar el nombre de “Pedidos” a “Pedidos Sitio Web” 
* Solución Desarrollada en la ruta ``` odoo-custom-addons>hnet_kitchen_control>static>src>xml>kitchen_pos_templates.xml```

```html
<tr>
    <td>
        <div class="control-button ver-pedidos" style="width: 80%; height: 100%; margin-top: 15px;">
            <span>
                <i class="fa fa-shopping-cart" aria-hidden="true"/>
                Pedidos Sitio Web
            </span>
        </div>
    </td>
</tr>
```

9. El botón de "Aplicar Propina" debe cambiar su nombre a "Eliminar Propina" cuando se haya aplicado la propina, en ambas formas se debe mostrar la previsualización de la factura 
* Solución Desarrollada en la ruta ``` odoo-custom-addons>hnet_kitchen_control>static>src>js>tip.js```

```js
printBill.BillScreenWidget.include({
    get_receipt_render_env: function(){

        var render_env = this._super();
        render_env.receipt.bill = true;
        var order = this.pos.get_order();

        //obtenemos lineas de orden
        var lines = order.get_orderlines();

        //Preparamos la propina
        var tip = this.pos.db.get_product_by_barcode("propina");
        var tip_line = false;

        //Ver si ya existe la linea de con la propina
        for (var line in lines){
            if(lines[line].product.id === tip.id){
                tip_line = lines[line];

            }
        }

        if($("#add-tip").html() == 'Aplicar Propina'){
            if(tip_line){
                console.log()
                order.remove_orderline(tip_line);
            }

            var subtotal = order.get_total_without_tax();

            order.add_product(tip, {
                price: Number.parseFloat(subtotal * 0.10).toFixed(2),
                quantity: 1,
                merge: false,
            });

            $("#add-tip").html('Eliminar Propina');

        }else{
            order.remove_orderline(tip_line);
            $("#add-tip").html('Aplicar Propina');
        }
        return render_env;

        },
     });
```

10. Bloquear el botón de notas para cualquier producto que ya haya sido ingresado a la cocina. Esta es una validación igual a las del punto #11, únicamente que con el botón de Notas. Ningún producto deberá poder borrarse o permitir cambiar cantidades después de haber sido enviado a la cocina. Solamente el usuario administrador tendrá esta función. Antes de ser ingresado a la cocina, los productos si deberán poder borrarse sin ningún problema. (Probar diferentes escenarios para validar este punto)

* 1er Parte de la Solución Desarrollada en la ruta ``` odoo-custom-addons>hnet_kitchen_control>static>src>js>kitchen__control_pos.js```

```js
// Agregar la clase 'note' al botón 'Notas'
var elem_note = $('[class="control-button"]');
var note_button = elem_note[0];
var html_note = $(note_button).html();
var content_note = (html_note.toString()).split('>');
var is_note = content_note[2].split('')

if((is_note.slice(1,5)).join('') == 'Nota'){
    $(note_button).addClass('note');
}
```

* 2da parte de la Solución Desarrollada en la ruta ``` odoo-custom-addons>hnet_kitchen_control>static>src>js>kitchen__control_pos.js```

```js
// Al hacer click en "Pedir" Agregar el id "note_tokitchen" al boton "Notas"
var note_button = $('[class="control-button note"]');
$(note_button).attr('id', 'note_tokitchen');
```

```js
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
```


11. Al momento de ingresar pedidos de delivery o pickup desde el Punto de Venta, el nombre del cliente dentro del pedido debe ser obligatorio. (puede crearse una dependencia entre el equipo de venta “delivery”, “pickup” y el campo del “cliente”). Luego de seleccionar el cliente de delivery consultar la referencia de orden. Si se quiere con cliente no se debe bloquear el botón de cliente

* 1er parte de la Solución Desarrollada en la ruta ``` odoo-custom-addons>hnet_kitchen_control>static>src>js>menu_hide_buttons.js```

```js
// Cargar popup de equipo de trabajo
if(current_table == 'Delivery' || current_table == 'delivery' || current_table == 'Deliveries' || current_table == 'deliveries'){
    if(this.pos.get_order()){
        var screen = this.pos.get_order().get_screen_data('screen');
        if(screen == 'products'){
            if(this.pos.get_order().delivery_filter){
                this.gui.show_screen('products');
            }else{
                this.gui.show_popup('PopupDeliveriesWidget');
            }
        }
    }
}
```

* 2da parte de la Solución Desarrollada en la ruta ``` odoo-custom-addons>hnet_kitchen_control>static>src>js>btn_pedidos_cocina.js```
    
```js
//Popup de deliveries
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
                this.pos.get_order().delivery_filter = filter;
                this.gui.show_screen('products');
            }
        }
     });
    gui.define_popup({name:'PopupDeliveriesWidget', widget: PopupDeliveriesWidget});
});
```

12. El dashboard de seguimiento de pedidos de cocina debe ser para control interno y meramente visual del estado de los pedidos. No debe incidir en ninguna validación del proceso de ventas. El dashboard deberá mostrar únicamente los pedidos de delivery o pickup del restaurante. Solamente tendrá 3 etapas: • Cocina • Facturación • Despachado


* Campos a mostrar
    * Número de orden 
    * Referencia (Pedido de delcocina) 
    * Origen (procedencia del pedido) 
    * Nombre del cliente 
    * Hora 
    * Acciones

* Acciones 
    * Mostrar pedido
        * Cancelar
        * Pasar a Facturación | Despachado


