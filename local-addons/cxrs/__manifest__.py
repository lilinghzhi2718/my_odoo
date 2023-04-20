# -*- coding: utf-8 -*-
{
    'name': "诚信二手2.0",

    'summary': """
       诚信二手
       """,

    'description': """
        诚信二手
    """,

    'author': "又菜又爱玩的克萨斯",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'data/ir.sequence.xml',
        'views/person.xml',
        'views/purchase.xml',
        'views/stock.xml',
        'views/product.xml',
        'views/sale.xml',
        'views/outstock.xml',
        'views/refundment.xml',
        'views/return_purchase.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application':True,
}
