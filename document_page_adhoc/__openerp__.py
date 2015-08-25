# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015  ADHOC SA  (http://www.adhoc.com.ar)
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
# Renombrado porque el modulo document_page todavia existe pero sin contenido
{
    'name': 'Document Page',
    'version': '8.0.1.0.1',
    'category': 'Knowledge Management',
    'description': """
Pages
=====
Web pages
    """,
    'author': ['OpenERP SA'],
    'website': 'http://www.openerp.com/',
    'depends': ['knowledge'],
    'data': [
        'wizard/document_page_create_menu_view.xml',
        'wizard/document_page_show_diff_view.xml',
        'document_page_view.xml',
        'security/document_page_security.xml',
        'security/ir.model.access.csv',
    ],
    'demo': ['document_page_demo.xml'],
    'test': ['test/document_page_test00.yml'],
    'installable': True,
    'auto_install': False,
    'images': [],
    'css' : ['static/src/css/document_page.css'],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
