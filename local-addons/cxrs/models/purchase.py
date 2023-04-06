from odoo import models, fields, api

class purchase(models.Model):

    _name = 'cxrs.purchase'
    _description='采购信息'
    _rec_name = 'purchase_ids'

    person_id=fields.Many2one('cxrs.person',string='供应者')
    purchase_ids = fields.Char(string='采购订单编号', readonly=True)
    product_name = fields.Char(string='货品名称',required=True)
    product_img = fields.Binary(string='货品图片')

    purchase_num = fields.Float(string='采购数量',default=1)
    purchase_cost = fields.Float(string='采购单价', required=True, digits=(8, 1))
    purchase_money = fields.Float(string='采购总价',compute='count_total',store=True,readonly=True,digits=(8,1))


    purchase_date = fields.Date(string='采购时间',default=fields.Date.today())
    purchase_detail = fields.Text(string='采购详情')


    color=fields.Integer()
    purchase_state = fields.Selection([('one','草稿'),('two','已验证'),('three','订单完成')],string='货品状态'
                                   ,readonly=True,default='one',copy=False,track_visiblity='onchange')


    def button_one(self):
        return self.write({"purchase_state":"one"})
    def button_two(self):
        return self.write({"purchase_state":"two"})
    def button_three(self):
        return self.write({"purchase_state":"three"})




    @api.model
    def create(self, vals):
        if not vals.get('purchase_ids'):
            vals['purchase_ids'] = self.env['ir.sequence'].next_by_code('cxrs.purchase.id') or '/'
        return super(purchase, self).create(vals)



    @api.depends('purchase_num','purchase_cost')
    def count_total(self):
        self.purchase_money = self.purchase_num * self.purchase_cost





