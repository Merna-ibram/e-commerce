from odoo import api, fields, models

class ResUsers(models.Model):
    _inherit = 'res.users'

    is_restricted_salesperson = fields.Boolean(
        string="Salesperson",
        help="If enabled, the user will only see their own Sale Orders."
    )

    #
    # @api.model
    # def search_fetch(self, domain, fields, offset=0, limit=None, order=None):
    #     user = self.env.user
    #
    #     if user.has_group('users.group_restricted_salesperson'):
    #         domain = expression.AND([
    #             domain,
    #             [('user_id', '=', user.id)]
    #         ])
    #     return super(ResUsers, self).search_fetch(domain, fields, offset=offset, limit=limit, order=order)

    # @api.onchange('is_restricted_salesperson')
    # def _onchange_is_restricted_salesperson(self):
    #     # UI hint فقط؛ الربط الحقيقي تحت في write/create
    #     pass
    #
    # def _get_restricted_group(self):
    #     return self.env.ref('users.group_restricted_salesperson')
    #
    # @api.model_create_multi
    # def create(self, vals_list):
    #     users = super().create(vals_list)
    #     group = self.env.ref('users.group_restricted_salesperson')
    #     for user, vals in zip(users, vals_list):
    #         if vals.get('is_restricted_salesperson'):
    #             user.groups_id = [(4, group.id)]
    #     return users
    #
    # def write(self, vals):
    #     res = super().write(vals)
    #     if 'is_restricted_salesperson' in vals:
    #         group = self._get_restricted_group()
    #         for user in self:
    #             if user.is_restricted_salesperson:
    #                 user.groups_id = [(4, group.id)]
    #             else:
    #                 user.groups_id = [(3, group.id)]
    #     return res
