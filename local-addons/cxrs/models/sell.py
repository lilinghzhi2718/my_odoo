from odoo import models, fields, api

class sell(models.Model):

    _name = 'cxrs.sell'
    _description='销售信息'
    _rec_name = 'product_name'


    #名称 货品编号 供应者编号 成本 采购时间 详情

    sell_id = fields.Char(string='销售订单编号',readonly=True)
    product_name = fields.Char(string='货品名称', required=True)
    sell_num = fields.Float(string='销售数量',default=1)
    sell_cost = fields.Float(string='销售单价', required=True, digits=(8, 1))
    sell_money=fields.Float(string='销售总价',compute='count_total',store=True,readonly=True,digits=(8,1))
    supplier=fields.Many2many('res.partner',string='购买者')
    product_img = fields.Binary(string='货品图片')


    sell_date = fields.Date(string='销售时间')
    sell_detail = fields.Text(string='详情')


    @api.model
    def create(self, vals):
        if not vals.get('sell_id'):
            vals['sell_id'] = self.env['ir.sequence'].next_by_code('cxrs.sell.id') or '/'
        return super(sell, self).create(vals)



    @api.depends('sell_num','sell_cost')
    def count_total(self):
        self. sell_money = self.sell_num * self.sell_cost