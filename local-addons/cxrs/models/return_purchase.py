from odoo import models, fields, api
from odoo.exceptions import ValidationError

class return_purchase(models.Model):
    _name = 'cxrs.return_purchase'
    _description = '采购退货'
    _rec_name = 'product_name'

    rp_pe_id = fields.Many2one('cxrs.person',string='顾客信息')
    rp_pr_id = fields.Many2one('cxrs.product', string='产品信息')
    rp_pu_id = fields.Many2one('cxrs.purchase', string='销售信息')

    product_name = fields.Char(string='货品名称')
    return_purchase_num = fields.Float(string='采购退货数量', default=0)


    return_purchase_date = fields.Datetime(string='采购退货时间', default=fields.Datetime.now())
    return_purchase_state = fields.Selection([('one', '草稿'), ('two', '已验证'), ('three', '退货出库')], string='退货状态'
                                  , readonly=True, default='one', copy=False, track_visiblity='onchange')

    color = fields.Integer()


    def button_one(self):
        return self.write({"return_purchase_state":"one"})

    def button_two(self):
         self.write({"return_purchase_state":"two"})
         self.return_purchase_date = fields.Datetime.now()
         purchase_record = self.env['cxrs.purchase'].browse(self.rp_pu_id.id)
         self.product_name = purchase_record.product_name
         if self.return_purchase_num > purchase_record.purchase_num:
                raise ValidationError('退款数量不能大于采购数量！')
         purchase_record.write({
        'purchase_num': purchase_record.purchase_num - self.return_purchase_num,
        'pu_rp_id': self.id,
    })

    def button_three(self):
        self.write({"return_purchase_state": "three"})
        product_record = self.env['cxrs.product'].browse(self.rp_pr_id.id)
        if self.return_purchase_num > product_record.product_num:
            raise ValidationError('出库数量不能大于库存数量！')
        product_record.write({
            'product_num': product_record.product_num - self.return_purchase_num,
            'pr_rp_id': self.id,
        })
