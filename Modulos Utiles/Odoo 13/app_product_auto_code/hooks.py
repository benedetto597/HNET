# -*- coding: utf-8 -*-

# Created on 2017-11-05
# author: 广州尚鹏，https://www.sunpop.cn
# email: 300883@qq.com
# resource of Sunpop
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# Odoo在线中文用户手册（长期更新）
# https://www.sunpop.cn/documentation/user/10.0/zh_CN/index.html

# Odoo10离线中文用户手册下载
# https://www.sunpop.cn/odoo10_user_manual_document_offline/
# Odoo10离线开发手册下载-含python教程，jquery参考，Jinja2模板，PostgresSQL参考（odoo开发必备）
# https://www.sunpop.cn/odoo10_developer_document_offline/
# description:

def pre_init_hook(cr):
    cr.execute("UPDATE product_product "
               "SET default_code = 'PN!' || id "
               "WHERE default_code IS NULL OR default_code = 'New';")

    cr.execute("UPDATE product_product "
               "SET barcode = default_code "
               "WHERE barcode IS NULL OR barcode = '';")

    cr.execute("UPDATE product_template "
               "Set default_code = "
               "(select default_code from product_product "
               "where product_product.product_tmpl_id = product_template.id limit 1)"
               "WHERE default_code IS NULL OR default_code = '' OR default_code = 'New';")

def post_init_hook(cr, registry):
    try:
        cr.execute("UPDATE product_category "
                   "SET ref = 'CAT!' || id "
                   "WHERE ref IS NULL OR ref = 'New';")
        pass
    except Exception as e:
        raise Warning(e)
