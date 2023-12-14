from odoo import fields, models, api

class ProductModel(models.Model):
    _name = "bnpi_product"
    _description = "Товар"
    _order = 'id desc'

    name = fields.Char('Наименование', required=True, )
    description = fields.Text('Текстовое описание')
    short_description = fields.Char('Короткое описание', compute='_compute_short_description')
    act_ids = fields.One2many('bnpi_act', 'product_id', 'Акты', )
    marked_product_ids = fields.One2many('bnpi_marked_product', 'product_id', 'Маркированные товары', )

    _sql_constraints = [
        ('name_uniq', 'UNIQUE (name)',
        'Название товара должно быть уникальным.'),
    ]

    @api.depends('description')
    def _compute_short_description(self):
        for product in self:
            if len(product.description) < 20:
                product.short_description = product.description
            else:
                index = product.description.find('\n')
                index = min( index if index > 0 else 21,  20)
                product.short_description = product.description[:index] + '...'
