from odoo import fields, models, api
import logging
logging.basicConfig(level=logging.INFO, filename="/opt/odoo/py_log.log", filemode="a")

class MarkedProductModel(models.Model):
    _name = "bnpi_marked_product"
    _description = "Товар"

    name = fields.Char(compute='_compute_name', string='Наименование')

    @api.depends('product_id')
    def _compute_name(self):
        for record in self:
            record.name = record.product_id.name + ' ' + str(record.id)

    product_id = fields.Many2one('bnpi_product', required=True, string='Товар')
    last_WH = fields.Text('Последний назначенный склад', required=True, )
    last_status = fields.Text('Последний назначенный статус', required=True, )
    acts_ids = fields.Many2many('bnpi_act', string='Акты')

    account_ids = fields.Many2many('bnpi_account', compute='_compute_accounts')

    @api.depends('acts_ids')
    def _compute_accounts(self):
        account_obj = self.env['bnpi_account']
        for marked_product in self:
            acc_ids = account_obj.search([('act_id', 'in', marked_product.acts_ids.ids)]).ids
            marked_product.account_ids = [(6, 0, acc_ids)]


