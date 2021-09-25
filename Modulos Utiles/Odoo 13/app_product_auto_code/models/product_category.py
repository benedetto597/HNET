# -*- coding: utf-8 -*-

# Created on 2017-11-28
# author: 广州尚鹏，https://www.sunpop.cn
# email: 300883@qq.com
# resource of Sunpop
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

# Odoo在线中文用户手册（长期更新）
# https://www.sunpop.cn/documentation/user/10.0/zh_CN/index.html

# Odoo10离线中文用户手册下载
# https://www.sunpop.cn/odoo10_user_manual_document_offline/
# Odoo10离线开发手册下载-含python教程，jquery参考，Jinja2模板，PostgresSQL参考（odoo开发必备）
# https://www.sunpop.cn/odoo10_developer_document_offline/
# description:

from odoo.osv import expression
from odoo import api, fields, models, exceptions, _

class ProductCategory(models.Model):
    _inherit = 'product.category'
    _order = 'sequence, ref'
    # 变更name 算法
    _rec_name = 'name'

    ref = fields.Char('Unique Code', index=True)
    sequence = fields.Integer('Sequence', help="Determine the display order")
    type = fields.Selection([
        ('consu', 'Consumable'),
        ('service', 'Service'),
        ('product', 'Stockable Product')], string='Default Product Type',
        help='Product in this category would set default type to this value.')

    sale_ok = fields.Boolean(
        'Default Can be Sold', default=True,
        help="Specify if the product can be selected in a sales order line.")
    purchase_ok = fields.Boolean('Default Can be Purchased', default=True)
    rental = fields.Boolean('Default Can be Rent')
    # Para instalar cuando un producto tiene el mismo código de barra que una variante
    barcode_auto = fields.Boolean('Default Barcode = Product Code', default=False)
    # 设置的当前目录用的 seq
    product_sequence_cur = fields.Many2one(
        'ir.sequence', 'Product Sequence',
        auto_join=True, domain="[('code', 'ilike', 'product.product')]")
    # 计算出来的 seq，当没有时自动使用上级的
    product_sequence = fields.Many2one(
        'ir.sequence', 'Product Sequence actual',
        compute='_compute_product_sequence',
        readonly=True)
    sequence_prefix = fields.Char('Sequence Prefix', related='product_sequence.prefix', readonly=True, store=False)
    tracking = fields.Selection([
        ('serial', 'By Unique Serial Number'),
        ('lot', 'By Lots'),
        ('none', 'No Tracking')], string="Default Tracking", default='none')

    # 增加目录编号唯一检查
    _sql_constraints = [
        ('uniq_ref',
         'unique(ref)',
         'The reference must be unique'),
    ]

    def _compute_product_sequence(self):
        for rec in self:
            if rec.product_sequence_cur:
                rec.product_sequence = rec.product_sequence_cur
            elif rec.parent_id:
                rec.product_sequence = rec.parent_id.product_sequence \
                    if rec.parent_id.product_sequence else self.env.ref('app_product_auto_code.seq_product_default', raise_if_not_found=False)
            else:
                rec.product_sequence = self.env.ref('app_product_auto_code.seq_product_default', raise_if_not_found=False)

    # 产品目录序号器，产生默认值，或者手工录入
    @api.model
    def default_get(self, fields):
        res = super(ProductCategory, self).default_get(fields)
        if 'ref' in res and res.ref != _('New'):
            pass
        else:
            try:
                res.update({'ref': self.env['ir.sequence'].next_by_code('product.category.default')})
            except Exception as e:
                pass
        return res

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        # 处理可以按ref和名称搜索
        args = args or []
        domain = []
        if name:
            domain = ['|', ('name', operator, name), ('ref', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]

        ids = self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)
        return self.browse(ids).name_get()

    # 当上级类别变化时，改变当前值
    @api.onchange('parent_id')
    def _onchange_parent_id(self):
        if self.parent_id:
            self.type = self.parent_id.type
            self.rental = self.parent_id.rental
            self.sale_ok = self.parent_id.sale_ok
            self.purchase_ok = self.parent_id.purchase_ok
            self.barcode_auto = self.parent_id.barcode_auto
            self.product_sequence_cur = self.parent_id.product_sequence_cur
            self.tracking = self.parent_id.tracking

    # 当传参 show_cat_name_short 时，只显示短目录名
    def name_get(self):
        try:
            if self._context.get('show_cat_name_short'):
                return [(value.id, "%s" % (value.name)) for value in self]
            else:
                return [(value.id, "%s" % (value.complete_name)) for value in self]
        except:
            return super(ProductCategory, self).name_get()


    def copy(self, default=None):
        # copy 时不要有 ref
        default = default or {}
        try:
            default['ref'] = self.env['ir.sequence'].next_by_code('product.category.default')
        except:
            pass
        return super(ProductCategory, self).copy(default)
