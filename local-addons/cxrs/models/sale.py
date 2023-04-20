from odoo import models, fields, api
from odoo.exceptions import ValidationError

class sale(models.Model):
    _name = 'cxrs.sale'
    _description = '销售订单'
    _rec_name = 'product_name'

    sa_pe_id = fields.Many2one('cxrs.person',string='顾客信息')
    sa_pr_id = fields.Many2one('cxrs.product', string='产品信息')
    sa_ou_id = fields.Many2one('cxrs.outstock', string='出库信息')
    sa_re_id = fields.Many2one('cxrs.refundment',string='退款信息')


    product_name = fields.Char(string='货品名称',required=True)
    product_img = fields.Binary(string='货品图片')
    product_num = fields.Float(string='货品数量', default=1)

    purchase_num = fields.Float(string='采购数量', default=1)

    sale_num = fields.Float(string='销售数量', default=1)
    sale_cost = fields.Float(string='售价', digits=(8, 1))
    sale_money = fields.Float(string='销售总价', compute='_compute_sale_money', store=True, readonly=True, digits=(8, 1))
    sale_date = fields.Datetime(string='销售时间', default=fields.Datetime.now())
    sale_detail = fields.Text(string='销售详情')
    sale_state = fields.Selection([('one', '草稿'), ('two', '已验证'), ('three', '订单完成')], string='货品状态'
                                  , readonly=True, default='one', copy=False, track_visiblity='onchange')

    color = fields.Integer()

    @api.depends('sale_num', 'sale_cost')
    def _compute_sale_money(self):
        for record in self:
            record.sale_money = record.sale_num * record.sale_cost

    def button_one(self):
        return self.write({"sale_state":"one"})
    def button_two(self):
        return self.write({"sale_state":"two"})
    def button_three(self):
        product_record = self.env['cxrs.product'].browse(self.sa_pr_id.id)
        product_record.write({
            'sale_money': self.sale_money,
            'pr_sa_id': self.id,
        })
        self.sale_date=fields.Datetime.now()
        self.write({"sale_state": "three"})
        outstock_form_id = self.env.ref('cxrs.cxrs_outstock_form_view').id
        return {
            'type': 'ir.actions.act_window',
            'name': '销售订单',
            'res_model': 'cxrs.outstock',
            'view_mode': 'form',
            'target': 'inline',
            'context': {
                'default_product_name': self.product_name,
                'default_product_img': self.product_img,
                'default_sale_num': self.sale_num,
            },
            'views': [(outstock_form_id, 'form')],
        }

    def button_four(self):
        person_form_id = self.env.ref('cxrs.cxrs_person_form_view').id
        return {
            'type': 'ir.actions.act_window',
            'name': '人物信息',
            'res_model': 'cxrs.person',
            'view_mode': 'form',
            'target': 'inline',
            'views': [(person_form_id, 'form')],
        }
    def button_five(self):
        refundment_form_id = self.env.ref('cxrs.cxrs_refundment_form_view').id
        return {
            'type': 'ir.actions.act_window',
            'name': '销售退货',
            'res_model': 'cxrs.refundment',
            'view_mode': 'form',
            'target': 'inline',
            'views': [(refundment_form_id, 'form')],
        }

    @api.model
    def create(self, vals):

        record = super(sale, self).create(vals)
        if 'default_product_name' in self.env.context:
            record.product_name = self.env.context['default_product_name']
        if 'default_product_img' in self.env.context:
            record.product_img = self.env.context['default_product_img']
        if 'default_purchase_num' in self.env.context:
            record.purchase_num = self.env.context['default_purchase_num']
        if 'default_product_num' in self.env.context:
            record.product_num = self.env.context['default_product_num']
        return record

    @api.constrains('sale_num')
    def _check_sale_num(self):
        for record in self:
            if record.sale_num > record.product_num:
                raise ValidationError('销售数量不能超过库存数量！')