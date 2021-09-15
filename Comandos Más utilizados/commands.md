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

* Obtener todos los records del modelo actual
```py
self.sudo().search([])
```

* Obtener un campo y multiples campos de un modelo especifico
```py
self.env['model.name'].search([('field1', '=', 'value')]).field2
```

* Forma eficiente de obtener un campo de un modelo especifico
```py
wt = self.env['model.name]
id_solicitado = wt.search([('field1', '=', 'value')]).id
nuevo = wt.browse(id_neded)
list = [new.field1, new.field2, new.field3]
```

* Obtener el último registro de una tabla
```py
last_id = self.env['model.name'].seach([])[-1].id
```

* Obtener las sesiones activas o abiertas
```py
running_sessions = self.env['pos.session'].sudo().search([('state', '!=', 'closed')])
```
* Obtener la sesión actual
```py
PosSession = self.env["pos.session"]
session_id = self.env.context.get('pos_session_id')
current_session = PosSession.browse(session_id)
```
* Dominio de busqueda con distintos valores de un mismo campo
```py
domain = [('state', 'in', ['paid','invoiced','done'])]
domain = AND([domain, [('session_id', 'in', session_ids)]])
orders = self.env['pos.order'].search(domain)
```
* Sobrescribir la función ***create*** de un modelo heredado
```py
class AccountJournal(models.Model):
    _inherit = "account.journal"

    @api.model
    def create(self, vals):
        rec = super(AccountJournal, self).create(vals)
        # ...        
        return rec
```
______
#### Frontend - JavaScript - XML 
* Imprimir en consola el recibo o factura acutal

```js   
console.log(this.receiptEnv.receipt);
```

* Cargar un modelo al POS
```js   
// Cargar equipos de ventas al POS
models.load_models([{
    model:  'crm.team',
    fields: ['name'],
    domain: function(self){ return [['cargar_pos', '=', true]]; },
    loaded: function(self, equipo_ventas) {
        self.equipo_ventas = equipo_ventas;
    }
}]);
```

* Imprimir en consola el recibo o factura acutal

```js
const order_id = self.db.add_order(order.export_as_JSON());
var order = self.db.get_order(order_id);
```

* Imprimir la clase widget en la consola del navegador 

```html
<!-- Imprimir JSON que produce la clase 'widget' -->
    <t t-set="wdgt" t-value="widget"/>
    <t t-esc="value"/>
    <t t-raw="value"/>
    <t t-field="odoo.value"/>
    <t t-js="odoo">
        console.log("Value", odoo.wdgt);
    </t>    
```

* Condicion a partir del modelo en el que se encuentra la clase widget

```html
<!-- Ocultar los botones a partir del modelo usando 'widget' -->
    <t t-if="widget.modelName != 'sale.order'">
        ```

* Pasar contexto en la llamada de una acción con un botón o link de una vista kanban 


```html
<!-- usando t-attf-data-context -->
<a style="margin-right: 10px" name="%(action_view_issues_of_task)d" type="action" t-attf-data-context="{'search_default_task_id': [active_id], 'default_task_id': active_id, 'default_project_id': project_id or False, 'default_partner_id': partner_id or False,}">
```
* Cambiar un atributo de un campo existente de un modelo existente - Se convierte en un campo requerido
```html
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <!-- El campo de equipo de venta en la orden de venta es obligatorio -->
        <record id="view_order_form_inherit_sale_stock" model="ir.ui.view">
            <field name="name">sale.order.form.sale.dropshipping</field>
            <field name="model">sale.order</field>
            <field name="inherit_id" ref="sale.view_order_form"/>
            <field name="arch" type="xml">
                <field name="team_id" position="attributes">
                    <attribute name="required">1</attribute>
                </field>
           </field>
        </record>
    </data>
</odoo>
```

* Agregar un action menu item

```html
<?xml version="1.0" encoding="UTF-8"?>
<openerp>
    <data>
        <!-- Your List View Definition -->
        <record id="view_your_model_name_tree" model="ir.ui.view">
            <field name="name">Your.Module.Name_tree</field>
            <field name="model">your.object</field>
            <field name="arch" type="xml">
                <tree string="ANY NAME">
                    <!-- Add All Fields You Want In The List Here -->
                    <field name="db_field_name"/>
                </tree>
            </field>
        </record>
        <!-- Your Form View Definition -->
        <record id="view_your_model_name_form" model="ir.ui.view">
            <field name="name">Your.Module.Name_form</field>
            <field name="model">your.object</field>
            <field name="arch" type="xml">
                <form string="Form View Name" version="7.0">
                    <!-- Add All Fields You Want In The Form Here -->
                    <field name="db_field_name"/>
                </form>
            </field>
        </record>
        <!-- Your Action Window Definition -->
        <record id="action_123" model="ir.actions.act_window">
            <field name="name">Your Module Name</field>
            <field name="res_model">your.object</field>
            <field name="view_type">form</field>
            <field name="view_mode">list,form</field>
        </record>
        <!-- Action Menu Item Related To Above Action Window -->
        <menuitem 
        action="action_123" 
        id="action_menu_123" 
        parent="write_the_parent_menu_id"
        name="Readable Text" 
        sequence="1"/>
    </data>
</openerp>
```