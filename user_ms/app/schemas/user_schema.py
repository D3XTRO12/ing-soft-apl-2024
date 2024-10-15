from app.models.user import User
from marshmallow import validate, fields, Schema, post_load

class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    dni = fields.String(required=True)
    email = fields.Email(required=True, validate=validate.Email())
    gender = fields.String(required=True, validate=validate.OneOf(['M', 'F']))
    age = fields.Integer(required=True)
    address = fields.String(required=True)
    phone = fields.String(required=True)
    role = fields.String(required=True, validate=validate.OneOf(['admin', 'user']))
    data = fields.Dict(required=False)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)
