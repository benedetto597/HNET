## Odoo 13 - Proyecto Furiwa
### Edgar Josué Benedetto Godoy
### 0801-1997-23600
#### ebenedetto@hnetw.com
#### edgar.benedetto@unah.hn
#### +504 3330-0171
#### 15/07/2021
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

```
 <t t-name="OrdersHistoryButton">
        <div class='control-button orders-history'>
            <i class='fa fa-list-alt '/> Historial Pagado
        </div>
    </t>
```

2. Cambiar "Seleccionar cajero" por "Seleccionar Personal" código encontrado en la ruta ``` odoo>addons>pos_hr>static>src>xml```

```
<span class="login-element">
    <button class="login-button select-employee">Seleccionar Personal</button>
</span>
```

3. Cambiar el nombre del botón "Reimprimir recibo" a "Reimprimir Prefactura" código encontrado en la ruta ``` odoo>addons>pos_reprint>static>src>xml>reprint.xml```

```
<t t-name="ReprintButton">
    <div class='control-button js_reprint'>
        <i class="fa fa-retweet"></i> Reimprimir Prefactura
    </div>
</t>
```

