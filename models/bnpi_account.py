from odoo import fields, models, api

class AccountModel(models.Model):
    _name = "bnpi_account"
    _description = "Счет"
    _order = "create_date"

    act_id = fields.Many2one('bnpi_act', string='Акт', ondelete='cascade')
    description = fields.Char('Затраты/Приходы', required=True,)
    value = fields.Integer('Значение, Р.', required=True,)