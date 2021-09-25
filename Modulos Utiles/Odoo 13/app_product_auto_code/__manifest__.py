# -*- coding: utf-8 -*-

# Created on 2019-01-04
# author: 广州尚鹏，https://www.sunpop.cn
# email: 300883@qq.com
# resource of Sunpop
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# Odoo12在线用户手册（长期更新）
# https://www.sunpop.cn/documentation/user/12.0/en/index.html

# Odoo12在线开发者手册（长期更新）
# https://www.sunpop.cn/documentation/12.0/index.html

# Odoo10在线中文用户手册（长期更新）
# https://www.sunpop.cn/documentation/user/10.0/zh_CN/index.html

# Odoo10离线中文用户手册下载
# https://www.sunpop.cn/odoo10_user_manual_document_offline/
# Odoo10离线开发手册下载-含python教程，jquery参考，Jinja2模板，PostgresSQL参考（odoo开发必备）
# https://www.sunpop.cn/odoo10_developer_document_offline/

{
    'name': 'Product Auto Sku Code,rule,barcode by Category, Variants Supported',
    'summary': """
    Product Auto code. Auto sku code. Auto Default Attributes. Unique code, auto Tracking Type.
    Product rule by category. 
    Product sort. Customize Sequence for category. like [raw-ipad-001],[raw-ipad-002]
    """,
    "version": '12.19.07.29',
    'category': 'Sales',
    'author': 'Sunpop.cn',
    'website': 'https://www.sunpop.cn',
    'license': 'AGPL-3',
    'sequence': 2,
    'installable': True,
    'auto_install': False,
    'application': True,
    'images': ['static/description/banner.png'],
    'currency': 'EUR',
    'price': 68,
    'description': """
        Best Product Auto code. Variants Supported. Auto Default Attributes. Unique code. Auto reference, unique reference.
                    
        This module allows to associate a sequence to the product reference by category.
        The reference (default code) is unique (SQL constraint) and required.
        Support Product with or without Variants.
        1. Auto code for every Product and Product Variants.自动产品编码。
        2. Get different sequence for different category.不同产品目录生成不同产品编码。
        3. Auto Code for every product variants, like product20181130-001.自动多规格产品编码，形式为 主产品编码-001。
        4. Product code must be Unique.产品编码强制要求唯一。
        5. Quick default value for every category. 按指定目录生成指定产品默认值，。
        6. Multi language support.多语种支持。
        7. Auto barcode. 自动生成条码。
        8. Drag to sort the Product sku show order. 产品可拖拽设置排序
        9. Input category code to search category in many2one select list. 在产品目录下拉选择中输入唯一编码定位相应的产品目录
        10.Fix category complete name bug for i18n. 修正产品目录名称的算法，在多语言下不会只显示英文
        11.Add 'show_cat_name_short' in context to show short name of category. 在context中加入'show_cat_name_short'即可只显示目录短名称
    """,
    'pre_init_hook': 'pre_init_hook',
    'post_init_hook': 'post_init_hook',
    'depends': [
        'product',
        'stock',
        # 'sale',
        # 'purchase',
        # 'mrp',
                ],
    'data': [
        # 视图
        'views/product_category_views.xml',
        'views/product_template_views.xml',
        'views/product_product_views.xml',
        'data/product_sequence_data.xml',
        'data/product_category_data.xml',
    ],
    'demo': [
    ],
}
