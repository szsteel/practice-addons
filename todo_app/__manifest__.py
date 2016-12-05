# -*- coding: utf-8 -*-
{
    'name': "To-Do Application",

    'summary': """
        Manage your personal tasks with this module.""",

    'description': """
        Manage your personal tasks with this module.
    """,

    'author': "Steel Chen",
    'website': "http://www.cognichain.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/todo_view.xml',
        'security/ir.model.access.csv',
        'security/todo_access_rules.xml',
    ],

    'application': True,
}
