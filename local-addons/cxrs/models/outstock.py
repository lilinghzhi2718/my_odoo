from odoo import models, fields, api
from odoo.exceptions import ValidationError

class outstock(models.Model):
    _name = 'cxrs.outstock'
    _description = '出库订单'
    _rec_name = 'product_name'

    ou_pe_id = fields.Many2one('cxrs.person',string='顾客信息')
    ou_pr_id = fields.Many2one('cxrs.product', string='产品信息')

    product_name = fields.Char(string='货品名称',required=True)
    product_img = fields.Binary(string='货品图片')
    outstock_num = fields.Float(string='出库数量', default=1)


    outstock_date = fields.Datetime(string='出库时间', default=fields.Datetime.now())
    outstock_state = fields.Selection([('one', '草稿'), ('two', '已验证'), ('three', '出库完成')], string='出库状态'
                                  , readonly=True, default='one', copy=False, track_visiblity='onchange')

    color = fields.Integer()


    def button_one(self):
        return self.write({"outstock_state":"one"})
    def button_two(self):
        return self.write({"outstock_state":"two"})
    def button_three(self):

        self.outstock_date=fields.Datetime.now()
        self.write({"outstock_state": "three"})
        product_record = self.env['cxrs.product'].browse(self.ou_pr_id.id)
        if self.outstock_num > product_record.product_num:
            raise ValidationError('出库数量不能大于库存数量！')
        product_record.write({
            'product_num': product_record.product_num - self.outstock_num,
            'outhand_date': fields.Datetime.now(),
            'pr_ou_id': self.id,
        })

    @api.model
    def create(self, vals):
        record = super(outstock, self).create(vals)
        if 'default_product_name' in self.env.context:
            record.product_name = self.env.context['default_product_name']
        if 'default_product_img' in self.env.context:
            record.product_img = self.env.context['default_product_img']
        if 'default_sale_num' in self.env.context:
            record.outstock_num = self.env.context['default_sale_num']
        return record


