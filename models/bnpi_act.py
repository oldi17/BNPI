from odoo import fields, models, api
from odoo.exceptions import ValidationError
import logging

class ActModel(models.Model):
    _name = "bnpi_act"
    _description = "Акт"
    _order = 'id desc'
    date = fields.Date('Дата документа', required=True, default=fields.Date.today())
    status = fields.Selection(string='Назначаемый статус', selection=[
        ('покупка', 'Покупка'),
        ('транспортировка', 'Транспортировка'),
        ('продажа', 'Продажа'),
    ], required=True, default='покупка')
    oldWH = fields.Char('Со склада',)
    newWH = fields.Char('На склад', required=True,)
    product_id = fields.Many2one('bnpi_product', 'Товар', ondelete="cascade")
    count = fields.Integer('Количество', default=1)
    marked_product_ids = fields.Many2many('bnpi_marked_product', string='Маркированные товары')
    account_ids = fields.One2many('bnpi_account', 'act_id', 'Счета', required=True, )
    confirmed = fields.Boolean('Подтверждено', default=False)

    _sql_constraints = [
        ('count_pos_check', 'CHECK (count > 0)',
        'Количество не должно быть меньше 1.'),
    ]

    @api.model
    def create(self, vals):
        res = super(ActModel, self).create(vals)
        if res.status != 'покупка':
            res.product_id = False
        else:
            res.marked_product_ids = False
        for account in res.account_ids:
            account.act_id = res.id
        return res
    
    def unlink(self):
        #your logic goes here
        marked_product_obj = self.env['bnpi_marked_product']
        for act in self:
            if act.status == 'покупка':
                marked_products = marked_product_obj.search(['id','in', act.marked_product_ids.ids])
                marked_products.unlink()
        return super(ActModel,self).unlink()
    
    def action_confirm(self):
        self.confirmed = True
        if self.status == 'покупка':
            for i in range(0, self.count):
                self.env['bnpi_marked_product'].create([
                    {
                        'product_id': self.product_id.id,
                        'last_WH': self.newWH,
                        'last_status': actStatusToMProductStatus(self.status),
                        'acts_ids': [self.id],
                    }]
                )
        else:
            for marked_product in self.marked_product_ids:
                marked_product.last_WH = self.newWH
                marked_product.last_status = actStatusToMProductStatus(self.status)


def actStatusToMProductStatus(actStatus: str):
    actStatuses = [
        'покупка',
        'транспортировка',
        'продажа',
    ]
    mProductStatuses = [
        'Куплен',
        'Транспортирован',
        'Продан',
    ]
    return mProductStatuses[actStatuses.index(actStatus)]