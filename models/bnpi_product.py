from odoo import fields, models, api

class ProductModel(models.Model):
    _name = "bnpi_product"
    _description = "Товар"

    name = fields.Char('Наименование', required=True, )
    description = fields.Text('Текстовое описание')
    act_ids = fields.One2many('bnpi_act', 'product_id', 'Акты', )
    marked_product_ids = fields.One2many('bnpi_marked_product', 'product_id', 'Маркированные товары', )

    _sql_constraints = [
        ('name_uniq', 'UNIQUE (name)',
        'Название товара должно быть уникальным.'),
    ]