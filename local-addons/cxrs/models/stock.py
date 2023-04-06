from odoo import models, fields, api

class stock(models.Model):
    _name = 'cxrs.stock'
    _description='仓库信息'
    _rec_name = 'stock_name'

    st_pr_id=fields.One2many('cxrs.product','pr_st_id',string='库存物品')
    stock_name = fields.Char(string='仓库名称', required=True)
    stock_ids = fields.Char(string='仓库编号', readonly=True)
    stock_local = fields.Char(string='仓库地址', required=True)

    @api.model
    def create(self, vals):
        if not vals.get('stock_ids'):
            vals['stock_ids'] = self.env['ir.sequence'].next_by_code('cxrs.stock.id') or '/'
        return super(stock, self).create(vals)