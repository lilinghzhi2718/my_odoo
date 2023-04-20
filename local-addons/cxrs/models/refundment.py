from odoo import models, fields, api
from odoo.exceptions import ValidationError

class refundment(models.Model):
    _name = 'cxrs.refundment'
    _description = '销售退货'
    _rec_name = 'product_name'

    re_pe_id = fields.Many2one('cxrs.person',string='顾客信息')
    re_pr_id = fields.Many2one('cxrs.product', string='产品信息')
    re_sa_id = fields.Many2one('cxrs.sale', string='销售信息')

    product_name = fields.Char(string='货品名称')
    refundment_num = fields.Float(string='销售退货数量', default=0)


    refundment_date = fields.Datetime(string='销售退货时间', default=fields.Datetime.now())
    refundment_state = fields.Selection([('one', '草稿'), ('two', '已验证'), ('three', '退货入库')], string='退货状态'
                                  , readonly=True, default='one', copy=False, track_visiblity='onchange')

    color = fields.Integer()


    def button_one(self):
        return self.write({"refundment_state":"one"})

    def button_two(self):
         self.write({"refundment_state":"two"})
         self.refundment_date = fields.Datetime.now()
         sale_record = self.env['cxrs.sale'].browse(self.re_sa_id.id)
         self.product_name = sale_record.product_name
         if self.refundment_num > sale_record.sale_num:
                raise ValidationError('退款数量不能大于销售数量！')
         sale_record.write({
        'sale_num': sale_record.sale_num - self.refundment_num,
        'sa_re_id': self.id,
    })

    def button_three(self):
        self.write({"refundment_state": "three"})
        product_record = self.env['cxrs.product'].browse(self.re_pr_id.id)
        if self.refundment_num > product_record.product_num:
            raise ValidationError('出库数量不能大于库存数量！')
        product_record.write({
            'product_num': product_record.product_num + self.refundment_num,
            'pr_re_id': self.id,
        })

