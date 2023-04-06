from odoo import models, fields, api

class person(models.Model):
    _name = 'cxrs.person'
    _description='人物信息'
    _rec_name = 'person_ids'
    purchase_id=fields.One2many('cxrs.purchase','person_id',string='收购物品')
    person_name = fields.Char(string='人物名称', required=True)
    person_ids = fields.Char(string='人物编号', readonly=True)
    person_wx = fields.Char(string='人物微信', required=True)
    person_tel = fields.Char(string='联系方式', required=True)
    person_img = fields.Binary(string='人物图片')
    color=fields.Integer()










    @api.model
    def create(self, vals):
        if not vals.get('person_ids'):
            vals['person_ids'] = self.env['ir.sequence'].next_by_code('cxrs.person.id') or '/'
        return super(person, self).create(vals)