##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.depends('uom_ids.sequence', 'uom_ids.purchase_ok')
    def _compute_uom_po_id(self):
        super()._compute_uom_po_id()
        for rec in self.filtered('uom_ids'):
            purchase_uoms = rec.uom_ids.filtered('purchase_ok').sorted().mapped('uom_id')
            if purchase_uoms:
                rec.uom_po_id = purchase_uoms[0]
