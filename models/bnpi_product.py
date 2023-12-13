from odoo import fields, models

class ProductModel(models.Model):
    _name = "bnpi_product"
    _description = "Товар"

    name = fields.Char('Наименование')
    description = fields.Text('Текстовое описание')
