from odoo import models, fields, api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    # حقل سعر مستقل لكل Variant
    variant_price = fields.Float(string="Variant Price")

    @api.depends('variant_price')
    def _compute_lst_price(self):
        for product in self:
            # لو فيه سعر محدد للـ variant، نستخدمه بدلاً من lst_price الافتراضي
            if product.variant_price:
                product.lst_price = product.variant_price

    def write(self, vals):
        if 'lst_price' in vals:
            # أي تعديل على lst_price للـ variant يروح على variant_price فقط
            vals['variant_price'] = vals.pop('lst_price')
        return super(ProductProduct, self).write(vals)

    @api.model
    def create(self, vals):
        if 'lst_price' in vals:
            vals['variant_price'] = vals.pop('lst_price')
        return super(ProductProduct, self).create(vals)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def _onchange_product_id_set_variant_price(self):
        if self.product_id and self.product_id.variant_price:
            self.price_unit = self.product_id.variant_price
        # لو مش فيه variant_price محدد، ممكن تستخدم lst_price العادي
        elif self.product_id:
            self.price_unit = self.product_id.lst_price
