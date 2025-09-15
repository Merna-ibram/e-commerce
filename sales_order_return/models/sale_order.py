from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sale_order_return_count = fields.Integer(compute='return_count')

    def return_count(self):
        for rec in self:
            rec.sale_order_return_count = self.env['sale.order.return'].search_count([
                ('sale_order_id', '=', rec.id)
            ])

    def action_open_return_wizard(self):
        # فلترة الخطوط اللي لسه فيها كمية قابلة للإرجاع
        returnable_lines = self.order_line.filtered(
            lambda line: line.product_uom_qty > line.return_qty
        )

        if not returnable_lines:
            raise UserError('لا يوجد منتجات متاحة للإرجاع.')

        return_order = self.env['sale.order.return'].create({
            'customer_id': self.partner_id.id,
            'sale_order_id': self.id,
        })

        # إنشاء خطوط الإرجاع حسب الكمية المتبقية
        for line in returnable_lines:
            qty_to_return = line.product_uom_qty - line.return_qty
            if qty_to_return > 0:
                self.env['sale.order.return.lines'].create({
                    'return_id': return_order.id,
                    'product_id': line.product_id.id,
                    'qty': qty_to_return,
                    'price_unit': line.price_unit
                })
                # تحديث الكمية المرتجعة
                line.return_qty += qty_to_return

        return {
            'name': 'Return Order',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order.return',
            'view_mode': 'form',
            'res_id': return_order.id,
            'target': 'current',
        }

    def View_return_order(self):
        return {
            'name': 'Sale Return',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order.return',
            'view_mode': 'list,form',
            'target': 'current',
            'domain': [('sale_order_id', '=', self.id)],
        }


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    return_qty = fields.Integer('Returned Quantity', default=0)
