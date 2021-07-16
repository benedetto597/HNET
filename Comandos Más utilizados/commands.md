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


