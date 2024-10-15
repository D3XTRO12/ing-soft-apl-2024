from app.models.category.category_model import Category
from marshmallow import fields, Schema, post_load

class CategorySchema(Schema):
    category_id = fields.Integer(dump_only = True)
    time_category = fields.String(required=True)
    tyre_type = fields.String(required=True)
    gender = fields.String(required=False)
    data = fields.Dict(required=False)
    
    @post_load
    def make_category(self, data, **kwargs):
        return Category(**data)