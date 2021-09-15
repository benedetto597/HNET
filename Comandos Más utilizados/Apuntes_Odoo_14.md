## Odoo Cookbook Dev 14 - HNET
### Edgar Josué Benedetto Godoy
### 0801-1997-23600
#### ebenedetto@hnetw.com
#### 11/09/2021
----------------------------------------------------------------
----------------------------------------------------------------

## Capitulo 03 - Creación de módulos complementarios de Odoo

### Organización de carpetas de un modulo
1. **models/** Contiene los archivos de código backend, creando así los modelos y sus lógica de negocios. Se recomienda un archivo por modelo con el mismo nombre que el modelo, por ejemplo, library_book.py para el modelo library.book. Estas se tratan en profundidad en el **Capítulo 4, Modelos de aplicación**.

2. **views/** Contiene los archivos XML para la interfaz de usuario, con las acciones, formularios, listas, etc. Al igual que los modelos, se recomienda tener un archivo por modelo. Nombres de archivo para Se espera que las plantillas de sitios web terminen con el sufijo _template. **Vistas de backend se explican en el Capítulo 9, Vistas de backend, y las vistas del sitio web se tratan en Capítulo 14, Desarrollo de sitios web de CMS**.

3. **data/** Contiene otros archivos de datos con los datos iniciales del módulo. **Los archivos de datos son explicado en el Capítulo 6, Gestión de datos del módulo.**

4. **demo/** Contiene archivos de datos con datos de demostración, que son útiles para pruebas,
formación o evaluación de módulos.

5. **i18n/** Es donde Odoo buscará los archivos .pot y .po de traducción. **Referirse a Capítulo 11, Internacionalización**, para más detalles. Estos archivos no necesitan ser mencionado en el archivo de manifiesto.

6. **security/** Contiene los archivos de datos que definen las listas de control de acceso, que generalmente es un archivo ir.model.access.csv y posiblemente un archivo XML para definir grupos de acceso y reglas de registro para la seguridad a nivel de fila. **Consulte el Capítulo 10, Acceso de seguridad**, para obtener más detalles al respecto.

7. **controllers/** Contiene los archivos de código para los controladores del sitio web y para los módulos que proporcionan ese tipo de función. **Los controladores web se tratan en el Capítulo 13, Desarrollo de servidores web.**
   
8. **static/** es donde se espera que se coloquen todos los activos web. A diferencia de otros directorios, este nombre de directorio no es solo una convención. Los archivos dentro de este directorio son públicos y se puede acceder a ellos sin un inicio de sesión de usuario. Este directorio contiene principalmente archivos como JavaScript, hojas de estilo e imágenes. No es necesario que se mencionen en el manifiesto del módulo, pero sí en la plantilla web. **Esto se analiza en detalle en el Capítulo 14, Desarrollo de sitios web de CMS**.

9. **wizard/** Contiene todos los archivos relacionados con los asistentes. En Odoo, se utilizan wizards para contener datos intermedios. Aprendemos más sobre **los asistentes en el Capítulo 8, Avanzado Técnicas de desarrollo del lado del servidor.**

10. **report/** Odoo proporciona una función para generar documentos PDF como ventas pedidos y facturas. Este directorio contiene todos los archivos relacionados con los informes en PDF. Aprenderemos más sobre **los informes PDF en el Capítulo 12, Automatización, Flujos de trabajo, Correos electrónicos e impresión.**
----------------------------------------------------------------
### Ejemplo de __manifest__.py

```py
{ 
    'name': "My library",
    'summary': "Manage books easily",
    'description': """ 
        Manage Library
        ==============
        Description related to library.
    """, 
    'author': "Your name", 
    'website': "http://www.example.com", 
    'category': 'Uncategorized', 
    'version': '13.0.1', 
    'depends': ['base'], 
    'data': ['views/views.xml'], 
    'demo': ['demo.xml'], 
} 
```

#### Definición de elementos y elementos extra del __manifest__.py

* **summary:** Este es el subtítulo con una descripción de una línea.

* **category:** Se utiliza para organizar los módulos por áreas de interés. La lista de nombres de categorías estándar disponibles se puede ver en https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml. Sin embargo, también es posible definir otros nombres de categorías nuevos aquí.

* **depends:** Esta es una lista con los nombres técnicos de los módulos de los que depende directamente. Si su módulo no depende de ningún otro módulo adicional, al menos debe agregar un módulo base. No olvide incluir cualquier módulo que defina ID, vistas o modelos XML a los que hace referencia este módulo. Eso asegurará que todos se carguen en el orden correcto, evitando errores difíciles de depurar.

* **data:** Esta es una lista de rutas relativas para que los archivos de datos se carguen durante la instalación o actualización del módulo. Las rutas son relativas al directorio raíz del módulo. Por lo general, estos son archivos XML y CSV, pero también es posible tener archivos de datos YAML. Estos se analizan en profundidad en el Capítulo 6, Gestión de datos del módulo.

* **aplication:** Si es Verdadero, el módulo aparece como una aplicación. Por lo general, se utiliza para el módulo central de un área funcional.

* **auto_install:** Si es Verdadero, indica que se trata de un módulo adhesivo, que se instala automáticamente cuando se instalan todas sus dependencias.

* **instalable:** Si es Verdadero (el valor predeterminado), indica que el módulo está disponible para la instalación.

* **external_dependencies:** Algunos módulos de Odoo utilizan internamente Python / binlibraries. Si sus módulos utilizan dichas bibliotecas, debe colocarlas aquí. Esto evitará que los usuarios instalen el módulo si los módulos enumerados no están instalados en la máquina host.

* **images:** Esto da el camino de las imágenes. Esta imagen se utilizará como imagen de portada en la tienda de aplicaciones de Odoo.

----------------------------------------------------------------

### Atributos principales del menuitem

* **name:** Este es el texto del elemento del menú que se mostrará.
* **action:** Es el identificador de la acción a ejecutar. Usamos el ID de la acción de ventana que creamos en el paso anterior.
* **sequence:** Se utiliza para establecer el orden en el que se presentan los elementos del menú del mismo nivel.
* **parent:** Este es el identificador del elemento del menú principal. Nuestro elemento de menú de ejemplo no tenía padre, lo que significa que se mostrará en la parte superior del menú.
* **web_icon:** Este atributo se utiliza para mostrar el icono del menú. Este icono solo se muestra en Odoo Enterprise Edition.

----------------------------------------------------------------

### Seguridad de Acceso

Al agregar un nuevo data model, debe definir quién puede **crear, leer, actualizar y eliminar registros.** Al crear una aplicación totalmente nueva, esto puede implicar la definición de nuevos grupos de usuarios. En consecuencia, si un usuario no tiene estos derechos de acceso, entonces Odoo no mostrará sus menús y vistas.
Esta receta se basa en el modelo del Libro de la biblioteca de las recetas anteriores y **define un nuevo grupo de seguridad de usuarios para controlar quién puede acceder o modificar los registros de los libros.**

#### Añadir regalas de seguridad (security rules)
* Todos podrán leer los registros de libros de la biblioteca.
* Un nuevo grupo de usuarios llamado Bibliotecarios tendrá derecho a crear, leer, actualizar y eliminar registros de libros.

1. Cree un archivo llamado ***security/groups.xml*** con el siguiente contenido

```html
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="group_librarian" model="res.groups">
        <field name="name">Librarians</field>
        <field name="users" eval="[(4, ref('base.user_
        admin'))]"/>
    </record>
</odoo>
```

2. Agregue un archivo llamado ***security/ir.model.access.csv*** con el siguiente contenido:

```csv
id,name,model_id:id,group_id:id,perm_read,perm_
write,perm_create,perm_unlink
acl_book,library.book default,model_library_book,,1,0,0,0
acl_book_librarian,library.book_librarian,model_library_
book,group_librarian,1,1,1,1
```
3. Agregue ambos archivos en la entrada de datos de __manifest__.py:

```py
# ... 
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/library_book.xml'
    ],
# ...
```
----------------------------------------------------------------

### Enlace con el código

[Código usado en el Capitulo 03 - Creación de módulos complementarios de Odoo](https://github.com/benedetto-hnet/Odoo-14-Development-Cookbook-Fourth-Edition/tree/master/Chapter03/06_access_rights/my_library)

----------------------------------------------------------------
----------------------------------------------------------------

## Capitulo 04 - Modelos de aplicación
### Obtener la representación de un registro

La representación de registros está disponible en un campo calculado mágico display_name y se ha agregado automáticamente a todos los modelos desde la versión 8.0. Sus valores se generan utilizando el método del modelo name_get (), que ya existía en las versiones anteriores de Odoo.
La implementación predeterminada de name_get () usa el atributo _rec_name para encontrar qué campo contiene los datos, que se usa para generar el nombre para mostrar. Si desea su propia implementación para el nombre de visualización, puede anular la lógica name_get () para generar un nombre de visualización personalizado. El método debe devolver una lista de tuplas con dos elementos: el ID del registro y la representación de cadena Unicode del registro.

* Por ejemplo, para tener el título y su fecha de estreno en la representación, como Moby Dick(1851-10-18), podemos definir lo siguiente:

```py
def name_get(self):
    result = []
    for record in self:
        rec_name = "%s (%s)" % (record.name, record.date_release)

        result.append((record.id, rec_name))
    return result
```

----------------------------------------------------------------

## Campos o fields y sus atributos

### Los tipos de campos no relacionales que están disponibles son los siguientes

* **Char** se utiliza para valores de cadena.
* **Text** se utiliza para valores de cadenas de varias líneas.
* **Selection** se utiliza para listas de selección. Tiene una lista de valores y pares de descripciones. El valor que se selecciona es lo que se almacena en la base de datos y puede ser una cadena o un número entero. La descripción se puede traducir automáticamente.
* **Html** es similar al campo de texto, pero se espera que almacene texto enriquecido en formato HTML.
* **Binary** almacenan archivos binarios, como imágenes o documentos.
* **Boolean** almacena valores verdaderos / falsos.
* **Date** almacena valores de fecha. Se almacenan en la base de datos como fechas. El ORM los maneja en forma de objetos de fecha de Python. Puede utilizar **fields.Date.today()** para establecer la **fecha actual** como un valor predeterminado en el campo de fecha.
* **Datetime** se utiliza para los valores de fecha y hora. Se almacenan en la base de datos en una fecha y hora ingenua, en hora UTC. El ORM los maneja en forma de objetos de fecha y hora de Python. Puede utilizar **fields.Date.now()** para establecer la **hora actual** como valor predeterminado en el campo de fecha y hora.
* **Integer** no necesitan más explicación.
* **Float** almacenan valores numéricos. Su precisión se puede definir opcionalmente con un número total de dígitos y pares de dígitos decimales.
* **Monetary** puede almacenar una cantidad en una determinada moneda. Esto también se explicará en la receta Agregar un campo monetario en este capítulo.

### Atributos de los campos no relacionales y relacionales

* **string** es el título del campo y se usa en las etiquetas de vista de la interfaz de usuario. Es opcional. Si no se establece, se derivará una etiqueta del nombre del campo agregando un caso de título y reemplazando los guiones bajos con espacios.
* **translate** cuando se establece en True, hace que el campo sea traducible. Puede tener un valor diferente, según el idioma de la interfaz de usuario.
* **default** es el valor predeterminado. También puede ser una función que se utiliza para calcular el valor predeterminado; por ejemplo, default = _compute_default, donde _compute_default es un método que se definió en el modelo antes de la definición del campo.
* **help** es un texto explicativo que se muestra en la información sobre herramientas de la interfaz de usuario.
* **groups** hace que el campo esté disponible solo para algunos grupos de seguridad. Es una cadena que contiene una lista separada por comas de ID XML para grupos de seguridad. Esto se trata con más detalle en el Capítulo 10, Acceso de seguridad.
* **states** permite que la interfaz de usuario establezca dinámicamente el valor de los atributos de solo lectura, obligatorios e invisibles, según el valor del campo de estado. Por lo tanto, requiere que exista un campo de estado y se use en la vista de formulario (incluso si es invisible). El nombre del atributo de estado está codificado en Odoo y no se puede cambiar.
* **copy** si el valor del campo se copia cuando se duplica el registro. De forma predeterminada, es Verdadero para campos no relacionales y Many2one, y False para One2many y campos calculados.
* **index**, cuando se establece en Verdadero, crea un índice de base de datos para el campo, lo que a veces permite búsquedas más rápidas. Reemplaza el atributo select = 1 obsoleto.
* **readonly** El indicador de solo lectura hace que el campo sea de solo lectura de forma predeterminada en la interfaz de usuario.
* **required** El indicador obligatorio hace que el campo sea obligatorio de forma predeterminada en la interfaz de usuario. Las diversas listas blancas que se mencionan aquí se definen en odoo / tools / mail.py.
* **company_dependent** El indicador de dependiente de la empresa hace que el campo almacene valores diferentes para cada empresa. Reemplaza el tipo de campo Propiedad en desuso.
* **group_operator** es una función agregada que se utiliza para mostrar resultados en el modo de grupo. Los valores posibles para este atributo incluyen count, count_distinct, array_agg, bool_and, bool_or, max, min, avg y sum. Los tipos de campo entero, flotante y monetario tienen la suma del valor predeterminado para este atributo.
* **sanitize** La bandera de desinfectar es utilizada por campos HTML y quita su contenido de etiquetas potencialmente inseguras. El uso de esto realiza una limpieza global de la entrada.


----------------------------------------------------------------
----------------------------------------------------------------

## Capitulo 08 - Técnicas avanzadas de desarrollo del lado del servidor 

### Pasos para crear un asistente o wizard para guiar al usuario

1. Agregue un nuevo modelo transitorio al módulo. Ejemplo:
```py
class LibraryRentWizard(models.TransientModel):     
    _name = 'library.rent.wizard'     
    
    borrower_id = fields.Many2one('res.partner',string='Borrower')     
    book_ids = fields.Many2many('library.book',string='Books')
```
