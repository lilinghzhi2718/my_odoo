from odoo import models, fields, api

class product(models.Model):

    _name = 'cxrs.product'
    _description='货品信息'
    _rec_name = 'product_name'


    #名称 货品编号 供应者编号 成本 采购时间 详情

    product_name = fields.Char(string='货品名称',required=True)
    product_id = fields.Char(string='货品编号',readonly=True)
    product_num = fields.Float(string='货品数量',default=1)
    product_img = fields.Binary(string='货品图片')
    product_money=fields.Float(string='物品总价',compute='count_total',store=True,readonly=True,digits=(8,1))
    supplier=fields.Many2many('res.partner',string='供应者')
    product_cost = fields.Float(string='货品成本',required=True,digits=(8,1))
    purchase_date = fields.Date(string='采购时间')
    product_detail = fields.Text(string='详情')
    product_state=fields.Selection([('on','在库'),('out','已出库'),('none','未入库')],string='货品状态'
                                   ,readonly=True,default='none',copy=False,track_visiblity='onchange')
    def button_on(self):
        return self.write({"product_state":"on"})
    def button_out(self):
        return self.write({"product_state":"out"})
    def button_none(self):
        return self.write({"product_state":"none"})





    @api.model
    def create(self, vals):
        if not vals.get('product_id'):
            vals['product_id'] = self.env['ir.sequence'].next_by_code('cxrs.product.id') or '/'
        return super(product, self).create(vals)



    @api.depends('product_num','product_cost')
    def count_total(self):
        self.product_money = self.product_num * self.product_cost
