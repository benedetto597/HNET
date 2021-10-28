# -*- coding: utf-8 -*-

# Created on 2018-10-30
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

from odoo import api, fields, models, exceptions, _


class ProductTemplate(models.Model):
    _inherit = ['product.template']
    _order = "sequence, name"

    default_code = fields.Char(
        'Internal Reference',
        compute='_compute_default_code',
        inverse='_set_default_code',
        store=True, default=lambda self: _('New'), copy=False)
    # 因为default_code有odoo的处理方式，影响面大，故会将其另存到 default_code_stored
    default_code_stored = fields.Char('Internal Reference Stored',
                                      default=lambda self: _('New'))

    # todo: 检查数据，要保证数据唯一性
    _sql_constraints = [
        ('uniq_default_code',
         'unique(default_code)',
         'The reference must be unique. Try save again.'),
    ]

    @api.model
    def default_get(self, fields):
        res = super(ProductTemplate, self).default_get(fields)
        # 内部编码类型默认值的录入
        if 'categ_id' in res:
            self._onchange_categ_id()
        return res

    @api.model
    def create(self, vals):
        cat = None
        if 'categ_id' in vals:
            cat = self.env['product.category'].search([('id', '=', vals['categ_id'])], limit=1)
        if 'attribute_line_ids' in vals:
            if len(vals['attribute_line_ids']) > 0:
                raise exceptions.ValidationError(_('Please save product first before adding varients!'))

        if 'default_code' not in vals or vals['default_code'] == _('New'):
            sequence = self.env.ref('app_product_auto_code.seq_product_default', raise_if_not_found=False)
            if cat and cat.product_sequence:
                sequence = cat.product_sequence
            try:
                vals['default_code'] = sequence.next_by_id()
            except:
                pass
        else:
            pass

        if vals['default_code']:
            vals['default_code_stored'] = vals['default_code']
        # 自动条码处理
        if cat and cat.barcode_auto and vals['default_code']:
            vals['barcode'] = vals['default_code']

        return super(ProductTemplate, self).create(vals)

    @api.depends('product_variant_ids', 'product_variant_ids.default_code')
    def _compute_default_code(self):
        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
        # 设置default_code
        for template in unique_variants:
            template.default_code = template.product_variant_ids.default_code
        for template in (self - unique_variants):
            if len(template.product_variant_ids) > 1 and template.default_code_stored:
                template.default_code = template.default_code_stored
                # template.default_code = ''


    def _set_default_code(self):
        self.ensure_one()
        if self.default_code:
            self.default_code_stored = self.default_code
        if len(self.product_variant_ids) == 1:
            self.product_variant_ids.default_code = self.default_code_stored

    # 当内部类型变化时，改变产品模板的各默认值
    @api.onchange('categ_id')
    def _onchange_categ_id(self):
        if self.categ_id:
            self.type = self.categ_id.type
            #self.rental = self.categ_id.rental
            self.sale_ok = self.categ_id.sale_ok
            self.purchase_ok = self.categ_id.purchase_ok
            self.tracking = self.categ_id.tracking
