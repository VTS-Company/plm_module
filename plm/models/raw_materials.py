# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class InventoryParts(models.Model):
    _name = "inventory.parts"
    _description = "the parts that form the products"

    name = fields.Text(string="part", required=True, unique=True)
    item_price = fields.Integer(string="item price", required=True)
    quantity = fields.Float(string="quantity", required=True)
    total_cost = fields.Integer(string="total price", readonly=True, compute="calculate_cost")
    storage = fields.Many2one("storage", string="storage Area")

    @api.constrains('item_price', 'quantity')
    def check_quantity(self):
        if self.item_price <= 0:
            raise ValidationError("السعر يجب ان يكون اكبر من صفر")
        elif self.quantity < 0:
            raise ValidationError("الكميه لا تكفي")

    @api.depends('item_price', 'quantity')
    def calculate_cost(self):
        self.total_cost = self.item_price * self.quantity

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "this part name already exists")
    ]


class Storage(models.Model):
    _name = "storage"
    _description = "the storage area of the product"

    name = fields.Text(string="Storage", required=True)
