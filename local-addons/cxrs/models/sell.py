from odoo import models, fields, api

class sell(models.Model):

    _name = 'cxrs.sell'
    _description='销售信息'
    _rec_name = 'product_name'


    #名称 货品编号 供应者编号 成本 采购时间 详情

    product_name = fields.Char(string='货品名称',required=True)
    sell_id = fields.Char(string='销售订单编号',readonly=True)
    sell_num = fields.Float(string='货品数量',default=1)
    product_img = fields.Binary(string='货品图片')
    sell_money=fields.Float(string='物品总价',compute='count_total',store=True,readonly=True,digits=(8,1))
    supplier=fields.Many2many('res.partner',string='购买者')
    product_sell = fields.Float(string='售出单价',required=True,digits=(8,1))
    sell_date = fields.Date(string='销售时间')
    sell_detail = fields.Text(string='详情')
    sell_state=fields.Selection([('one','草稿'),('two','确认订单'),('three','支付成功')],string='销售状态'
                                   ,readonly=True,default='none',copy=False,track_visiblity='onchange')
    def button_one(self):
        return self.write({"product_state":"one"})
    def button_two(self):
        return self.write({"product_state":"two"})
    def button_three(self):
        return self.write({"product_state":"three"})





    @api.model
    def create(self, vals):
        if not vals.get('sell_id'):
            vals['sell_id'] = self.env['ir.sequence'].next_by_code('cxrs.sell.id') or '/'
        return super(sell, self).create(vals)



    @api.depends('sell_num','product_sell')
    def count_total(self):
        self. sell_money = self.sell_num * self.product_sell