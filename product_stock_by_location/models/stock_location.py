##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import fields, models, api


class StockLocation(models.Model):

    _inherit = 'stock.location'

    show_stock_on_products = fields.Boolean(
        help='If true, this location will be shown on the pop up window opened'
        'from products kanban and tree view'
    )
    qty_available = fields.Float(
        compute='_compute_product_available',
        digits='Product Unit of Measure',
        string='Quantity On Hand',
        help="Current quantity of products.\n"
             "In a context with a single Stock Location, this includes "
             "goods stored at this Location, or any of its children.\n"
             "In a context with a single Warehouse, this includes "
             "goods stored in the Stock Location of this Warehouse, or any "
             "of its children.\n"
             "stored in the Stock Location of the Warehouse of this Shop, "
             "or any of its children.\n"
             "Otherwise, this includes goods stored in any Stock Location "
             "with 'internal' type."
    )
    virtual_available = fields.Float(
        compute='_compute_product_available',
        digits='Product Unit of Measure',
        string='Forecast Quantity',
        help="Forecast quantity (computed as Quantity On Hand "
             "- Outgoing + Incoming)\n"
             "In a context with a single Stock Location, this includes "
             "goods stored in this location, or any of its children.\n"
             "In a context with a single Warehouse, this includes "
             "goods stored in the Stock Location of this Warehouse, or any "
             "of its children.\n"
             "Otherwise, this includes goods stored in any Stock Location "
             "with 'internal' type."
    )
    incoming_qty = fields.Float(
        compute='_compute_product_available',
        digits='Product Unit of Measure',
        string='Incoming',
        help="Quantity of products that are planned to arrive.\n"
             "In a context with a single Stock Location, this includes "
             "goods arriving to this Location, or any of its children.\n"
             "In a context with a single Warehouse, this includes "
             "goods arriving to the Stock Location of this Warehouse, or "
             "any of its children.\n"
             "Otherwise, this includes goods arriving to any Stock "
             "Location with 'internal' type."
    )
    outgoing_qty = fields.Float(
        compute='_compute_product_available',
        digits='Product Unit of Measure',
        string='Outgoing',
        help="Quantity of products that are planned to leave.\n"
             "In a context with a single Stock Location, this includes "
             "goods leaving this Location, or any of its children.\n"
             "In a context with a single Warehouse, this includes "
             "goods leaving the Stock Location of this Warehouse, or "
             "any of its children.\n"
             "Otherwise, this includes goods leaving any Stock "
             "Location with 'internal' type."
    )

    @api.depends_context('product_id', 'template_id')
    def _compute_product_available(self):
        template_id = []
        product_id = []
        if self._context.get('active_model', False) == 'product.template':
            template_id = self._context.get('active_id', False)
        elif self._context.get('active_model', False) == 'product.product':
            product_id = self._context.get('active_id', False)
        if template_id:
            product_variants = self.env['product.template'].browse(template_id).product_variant_ids
        elif product_id:
            product_variants = self.env['product.product'].browse(product_id)
        else:
            # it not template_id or product_id on context, return True
            for rec in self:
                rec.qty_available = 0
                rec.virtual_available = 0
                rec.incoming_qty = 0
                rec.outgoing_qty = 0
            return True
        for rec in self:
            product_variants = [p.with_context(location=rec.id) for p in product_variants]
            rec.qty_available = sum(p.qty_available for p in product_variants)
            rec.virtual_available = sum(p.virtual_available for p in product_variants)
            rec.incoming_qty = sum(p.incoming_qty for p in product_variants)
            rec.outgoing_qty = sum(p.outgoing_qty for p in product_variants)
