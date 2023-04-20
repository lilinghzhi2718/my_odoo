from odoo import models, fields, api

class product(models.Model):

    _name = 'cxrs.product'
    _description='物品信息'
    _rec_name = 'product_name'

    pr_ou_id = fields.Many2one('cxrs.outstock', string='出库信息')
    pr_sa_id = fields.Many2one('cxrs.sale', string='销售信息')
    pr_pe_id = fields.Many2one('cxrs.person', string='供应商信息')
    pr_pu_id=fields.Many2one('cxrs.purchase',string='采购信息')
    pr_re_id=fields.Many2one('cxrs.refundment', string='销售退货信息')
    pr_rp_id = fields.Many2one('cxrs.return_purchase', string='采购退货信息')

    product_ids = fields.Char(string='货品编号', readonly=True)
    product_name = fields.Char(string='货品名称',required=True)
    product_img = fields.Binary(string='货品图片')
    product_num = fields.Float(string='货品数量', default=0)

    sale_num = fields.Float(string='销售数量', default=0)
    sale_cost = fields.Float(string='售价',digits=(8, 1))
    sale_money = fields.Float(string='销售总价', compute='count_sale_money', store=True, readonly=True, digits=(8, 1))
    sale_date = fields.Datetime(string='销售时间',default=fields.Datetime.now())
    sale_detail = fields.Text(string='销售详情')

    purchase_ids = fields.Char(string='采购订单编号', readonly=True)
    purchase_num = fields.Float(string='采购数量',default=1)
    purchase_cost = fields.Float(string='采购单价',digits=(8, 1))
    purchase_money = fields.Float(string='采购总价',compute='count_purchase_money',store=True,readonly=True,digits=(8,1))
    purchase_detail = fields.Text(string='采购详情')

    onhand_date=fields.Datetime(string='入库时间')
    outhand_date = fields.Datetime(string='出库时间')
    purchase_date = fields.Datetime(string='采购时间')

    pr_st_id = fields.Many2one('cxrs.stock', string='仓库')
    zone_ids = fields.Selection(selection=[('A', 'A区'), ('B', 'B区'), ('C', 'C区')],
                                   string="所在区域")
    rack_ids = fields.Selection(selection=[('a', '001'), ('b', '002'), ('c', '003')],
                                   string="所在货架")


    color=fields.Integer()

    product_state = fields.Selection([('one','草稿'),('two','运输中'),('three','已入库')],string='货品状态'
                                   ,readonly=True,default='one',copy=False,track_visiblity='onchange')



    def button_one(self):
        return self.write({"product_state":"one"})

    def button_two(self):
        return self.write({"product_state":"two"})
    def button_three(self):
        self.onhand_date=fields.Datetime.now()
        return self.write({"product_state":"three"})

    def button_four(self):
        sale_form_id = self.env.ref('cxrs.cxrs_sale_form_view').id
        return {
            'type': 'ir.actions.act_window',
            'name': '销售订单',
            'res_model': 'cxrs.sale',
            'view_mode': 'form',
            'target': 'inline',
            'context': {
                'default_product_name': self.product_name,
                'default_product_img': self.product_img,
                'default_purchase_num': self.purchase_num,
                'default_product_num': self.product_num,
            },
            'views': [(sale_form_id, 'form')],
        }



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
    def count_purchase_money(self):
        self.purchase_money = self.purchase_num * self.purchase_cost

    @api.depends('sale_num', 'sale_cost')
    def count_sale_money(self):
        self.sale_money = self.sale_num * self.sale_cost

    @api.depends('sale_num', 'purchase_num')
    def count_product_num(self):
        self.product_num = self.purchase_num - self.sale_num


