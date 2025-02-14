##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    def _get_products_price(
            self, products, quantity, date=False, uom_id=False, **kwargs):
        """If we send taxes_included on context we include price on the
        requested prices for this pricelist. We do it here and not in
        price_compute of product.template / product.product because:
        * we only need to do it once
        * pricelist could be based on fixed prices so product price is not used
        """
        res = super()._get_products_price(
            products, quantity, date=date, uom_id=uom_id, **kwargs)
        if self._context.get('taxes_included'):
            company_id = (self._context.get('company_id')
                          or self.env.company.id)
            for product in products:
                # for compatibility with product_pack
                if 'pack_ok' in product._fields and self.check_for_product_pack_parent(product):
                    continue
                res[product.id] = product.taxes_id.filtered(
                    lambda x: x.company_id.id == company_id).compute_all(
                        res[product.id], product=product)['total_included']
        return res

    def check_for_product_pack_parent(self, product):
        """
        we use this method to handler several situation for product pack and pricelist 
        We always return False (to continue with the calculation) except for some situation below
        """
        result = False
        if product.pack_ok and product.pack_component_price != 'ignored':
            if product._name == 'product.template' and product in self.item_ids.mapped('product_tmpl_id'):
                result = False
            elif product._name == 'product.product' and (product in self.item_ids.mapped('product_id') or product.product_tmpl_id in self.item_ids.mapped('product_tmpl_id')):
                result = False
            else:
                result = True
        return result

    def _get_product_price(self, product, *args, **kwargs):
        res = super(ProductPricelist, self.with_context(is_recursive=True))._get_product_price(product, *args, **kwargs)
        if self._context.get('taxes_included') and not self._context.get('is_recursive'):
            company_id = (self._context.get('company_id')
                          or self.env.company.id)
            res = product.taxes_id.filtered(
                lambda x: x.company_id.id == company_id).compute_all(res, product=product)['total_included']
        return res
