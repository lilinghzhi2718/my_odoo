from odoo import models, fields, api

class product(models.Model):

    _name = 'cxrs.product'
    _description='物品信息'

    pr_pe_id = fields.Many2one('cxrs.person', string='供应商信息')
    pr_pu_id=fields.Many2one('cxrs.purchase',string='采购信息')

    product_ids = fields.Char(string='货品编号', readonly=True)
    product_name = fields.Char(string='货品名称',required=True)
    product_img = fields.Binary(string='货品图片')
    product_num = fields.Float(string='货品数量', default=1)
    sale_num = fields.Float(string='货品数量', default=1)
    sale_cost = fields.Float(string='物品售价',digits=(8, 1))
    sale_money = fields.Float(string='销售总价', compute='count_total', store=True, readonly=True, digits=(8, 1))

    purchase_ids = fields.Char(string='采购订单编号', readonly=True)
    purchase_num = fields.Float(string='采购数量',default=1)
    purchase_cost = fields.Float(string='采购单价',digits=(8, 1))
    purchase_money = fields.Float(string='采购总价',compute='count_total',store=True,readonly=True,digits=(8,1))
    purchase_detail = fields.Text(string='采购详情')

    onhand_date=fields.Date(string='入库时间',default=fields.Date.today())
    outhand_date = fields.Date(string='出库时间', default=fields.Date.today())
    purchase_date = fields.Date(string='采购时间',default=fields.Date.today())

    pr_st_id = fields.Many2one('cxrs.stock', string='仓库')
    zone_ids = fields.Selection(selection=[('A', 'A区'), ('B', 'B区'), ('C', 'C区')],
                                   string="所在区域")
    rack_ids = fields.Selection(selection=[('a', '001'), ('b', '002'), ('c', '003')],
                                   string="所在货架")


    color=fields.Integer()
    product_state = fields.Selection([('one','草稿'),('two','运输中'),('three','已入库'),('four','已出库')],string='货品状态'
                                   ,readonly=True,default='one',copy=False,track_visiblity='onchange')


    def button_one(self):
        return self.write({"product_state":"one"})
    def button_two(self):
        return self.write({"product_state":"two"})
    def button_three(self):
        return self.write({"product_state":"three"})
    def button_four(self):
        return self.write({"product_state":"four"})




    @api.model
    def create(self, vals):
        if not vals.get('product_ids'):
            vals['product_ids'] = self.env['ir.sequence'].next_by_code('cxrs.product.id') or '/'
        record = super(product, self).create(vals)
        if 'default_purchase_ids' in self.env.context:
            record.purchase_ids = self.env.context['default_purchase_ids']
        if 'default_product_name' in self.env.context:
            record.product_name = self.env.context['default_product_name']
        if 'default_product_img' in self.env.context:
            record.product_img = self.env.context['default_product_img']
        if 'default_purchase_num' in self.env.context:
            record.purchase_num = self.env.context['default_purchase_num']
            record.product_num = self.env.context['default_purchase_num']
        if 'default_purchase_cost' in self.env.context:
            record.purchase_cost = self.env.context['default_purchase_cost']
        if 'default_purchase_money' in self.env.context:
            record.purchase_money = self.env.context['default_purchase_money']
        if 'default_purchase_date' in self.env.context:
            record.purchase_date = self.env.context['default_purchase_date']
        return record

    @api.depends('purchase_num','purchase_cost')
    def count_total(self):
        self.purchase_money = self.purchase_num * self.purchase_cost

    @api.depends('sale_num', 'sale_cost')
    def count_total(self):
        self.sale_money = self.sale_num * self.sale_cost
