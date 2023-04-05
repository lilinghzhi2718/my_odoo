# -*- coding: utf-8 -*-
# from odoo import http


# class Cxrs(http.Controller):
#     @http.route('/cxrs/cxrs', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cxrs/cxrs/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('cxrs.listing', {
#             'root': '/cxrs/cxrs',
#             'objects': http.request.env['cxrs.cxrs'].search([]),
#         })

#     @http.route('/cxrs/cxrs/objects/<model("cxrs.cxrs"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cxrs.object', {
#             'object': obj
#         })
