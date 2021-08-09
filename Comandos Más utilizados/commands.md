## Curso Técnico de Odoo Starter-Udemy-HNET
### Edgar Josué Benedetto Godoy
### 0801-1997-23600
#### ebenedetto@hnetw.com
#### edgar.benedetto@unah.hn
#### +504 3330-0171
#### 13/07/2021
___
___
# Comandos más utilizados
___
### Entorno de trabajo - venv
* Active el entorno con el siguiente comando:

```
source odoo-venv/bin/activate
```

* Desactivar el entorno con el siguiente comando:

```
deactivate
```

* Resolver problemas de permisos en ambiente virtual
```
sudo chown -R your_username:your_username path/to/virtuaelenv/
```

* Instalar las dependencias del archivo de dependencias de odoo
```
pip3 install -r odoo/requirements.txt
```

### Eliminar Odoo por completo 

* STOP SERVER
```
sudo service odoo stop

sudo service odoo-server stop
```

* REMOVE ALL ODOO FILES

```
sudo rm -R /opt/odoo
```

* REMOVE CONFIG FILES

```
sudo rm -f /etc/odoo.conf

sudo rm -f /etc/odoo/odoo.conf

sudo rm -f /etc/odoo-server.conf 

sudo rm -f /etc/systemd/system/odoo13.service

sudo update-rc.d -f odoo remove

sudo update-rc.d -f odoo-server remove 

sudo rm -f /etc/init.d/odoo 

sudo rm -f /etc/init.d/odoo-server 
```

* REMOVE USER AND USER GROUP

```
sudo userdel -r postgres

sudo groupdel postgres
```

* REMOVE DATABASE
```
sudo apt-get remove postgresql -y

sudo apt-get --purge remove postgresql\* -y

sudo rm -rf /etc/postgresql/

sudo rm -rf /etc/postgresql-common/

sudo rm -rf /var/lib/postgresql/
```

### Base de Datos - PostgreSQL 
* Resolver error de autenticación --> Error: FATAL: Peer authentication failed for user "odoo 14"
    1. Modificar el archivo de conf de postgresql 
        ```
        sudo nano /etc/postgresql/9.3/main/pg_hba.conf
        ```
    2. Agregar el comando para que todo el trafico del usuario odoo14 sea admitido
        ```
        local all user_name trust

        local all odoo14 trust
        ```
    3. Reiniciar Servidor postgresql
        ```
        sudo service postgresql restart
        ```

______
______
### Odoo 13
#### Backend - Python
_____
#### Frontend - JavaScript - XML

* Botón personalizado Odoo v13

```js
odoo.define('custom-button.custom_button', function (require) {
"use strict";
    var core = require('web.core');
    var screens = require('point_of_sale.screens');
    var gui = require('point_of_sale.gui');

    //Custom Code
    var CustomButton = screens.ActionButtonWidget.extend({
        template: 'CustomButton',

        button_click: function(){

        var self = this;
        self.custom_function();
        
        },

        custom_function: function(){
            console.log('Hi I am button click of CustomButton');
        }

    });

    screens.define_action_button({
        'name': 'custom_button',
        'widget': CustomButton,
    });
});
```

```html
<!-- static > src > xml -->
<?xml version="1.0" encoding="UTF-8"?>
<templates id="template" xml:space="preserve">
    <t t-name="CustomButton">
        <span class="control-button">
            <i class="fa fa-print"></i>
            Custom Button
        </span>
    </t>

</templates>
```

```html
<!-- views -->
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <template id="assets" inherit_id="point_of_sale.assets">
        <xpath expr="." position="inside">
            <script type="text/javascript" src="/custom-button/static/src/js/custom.js"></script>
        </xpath>
    </template>
</odoo>
```
_______
_______
### Odoo v14
#### Backend - Python
* Crear y actualizar ordenes de venta desde el fronted con py

``` python
@api.model
    def create_from_ui(self, orders, draft=False):
        """ Create and update Orders from the frontend PoS application.

        Create new orders and update orders that are in draft status. If an order already exists with a status
        diferent from 'draft'it will be discareded, otherwise it will be saved to the database. If saved with
        'draft' status the order can be overwritten later by this function.

        :param orders: dictionary with the orders to be created.
        :type orders: dict.
        :param draft: Indicate if the orders are ment to be finalised or temporarily saved.
        :type draft: bool.
        :Returns: list -- list of db-ids for the created and updated orders.
        """
        order_ids = []
        for order in orders:
            existing_order = False
            if 'server_id' in order['data']:
                existing_order = self.env['pos.order'].search(['|', ('id', '=', order['data']['server_id']), ('pos_reference', '=', order['data']['name'])], limit=1)
            if (existing_order and existing_order.state == 'draft') or not existing_order:
                order_ids.append(self._process_order(order, draft, existing_order))

        return self.env['pos.order'].search_read(domain = [('id', 'in', order_ids)], fields = ['id', 'pos_reference'])
```
______
#### Frontend - JavaScript - XML 
* Imprimir en consola el recibo o factura acutal

```js   
console.log(this.receiptEnv.receipt);
```

* Imprimir en consola el recibo o factura acutal

```js
const order_id = self.db.add_order(order.export_as_JSON());
var order = self.db.get_order(order_id);
```
