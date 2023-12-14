from odoo import fields, models, api

class MarkedProductModel(models.Model):
    _name = "bnpi_marked_product"
    _description = "Товар"

    name = fields.Char(compute='_compute_name', string='Наименование')
    product_id = fields.Many2one('bnpi_product', required=True, string='Товар', ondelete="cascade")
    last_WH = fields.Text('Склад', required=True, )
    last_status = fields.Text('Статус', required=True, )
    acts_ids = fields.Many2many('bnpi_act', string='Акты')
    account_ids = fields.Many2many('bnpi_account', compute='_compute_accounts')
    total = fields.Integer(string='Прибыль', compute='_compute_total')

    @api.depends('product_id')
    def _compute_name(self):
        for record in self:
            record.name = record.product_id.name + ' ' + str(record.id)

    @api.depends('acts_ids')
    def _compute_accounts(self):
        account_obj = self.env['bnpi_account']
        act_obj = self.env['bnpi_act']
        for marked_product in self:
            ids = act_obj.search([
                ('id', 'in', marked_product.acts_ids.ids),
                ('confirmed', '=', True)
            ]).ids
            acc_ids = account_obj.search([('act_id', 'in', ids)]).ids
            marked_product.account_ids = [(6, 0, acc_ids)]
    
    @api.depends('account_ids')
    def _compute_total(self):
        for marked_product in self:
            res = 0
            for account in marked_product.account_ids:
                res += account.value
            marked_product.total = res


