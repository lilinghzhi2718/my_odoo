from odoo import models, fields, api

class purchase(models.Model):

    _name = 'cxrs.purchase'
    _description='采购信息'
    _rec_name = 'purchase_ids'




    pu_pr_id = fields.One2many('cxrs.product', 'pr_pu_id', string='收购物品')
    pu_pe_id=fields.Many2one('cxrs.person',string='人物名称',index=True,display_name='pu_pe_id.person_name')

    purchase_ids = fields.Char(string='采购订单编号', readonly=True)
    product_name = fields.Char(string='货品名称',required=True)
    product_img = fields.Binary(string='货品图片')
    purchase_num = fields.Float(string='采购数量',default=1)
    purchase_cost = fields.Float(string='采购单价', required=True, digits=(8, 1))
    purchase_money = fields.Float(string='采购总价',compute='count_total',store=True,readonly=True,digits=(8,1))

    purchase_date = fields.Datetime(string='采购时间',default=fields.Datetime.now())
    purchase_detail = fields.Text(string='采购详情')


    color=fields.Integer()
    purchase_state = fields.Selection([('one','草稿'),('two','已验证'),('three','订单完成')],string='货品状态'
                                   ,readonly=True,default='one',copy=False,track_visiblity='onchange')


    def button_one(self):
        return self.write({"purchase_state":"one"})
    def button_two(self):
        return self.write({"purchase_state":"two"})
    def button_three(self):
        self.write({"purchase_state":"three"})
        product_form_id = self.env.ref('cxrs.cxrs_product_form_view').id
        return {
            'type': 'ir.actions.act_window',
            'name': '入库单',
            'res_model': 'cxrs.product',
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_purchase_ids': self.purchase_ids,
                'default_product_name': self.product_name,
                'default_product_img': self.product_img,
                'default_purchase_num': self.purchase_num,
                'default_purchase_cost': self.purchase_cost,
                'default_purchase_money': self.purchase_money,
                'default_purchase_date': self.purchase_date,
            },
            'views': [(product_form_id, 'form')],
        }




    @api.model
    def create(self, vals):
        if not vals.get('purchase_ids'):
            vals['purchase_ids'] = self.env['ir.sequence'].next_by_code('cxrs.purchase.id') or '/'
        return super(purchase, self).create(vals)



    @api.depends('purchase_num','purchase_cost')
    def count_total(self):
        self.purchase_money = self.purchase_num * self.purchase_cost







