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
