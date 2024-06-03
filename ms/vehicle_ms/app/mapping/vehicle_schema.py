from app.models.vehicle.vehicle_model import Vehicle
from marshmallow import fields, Schema, post_load

class VehicleSchema(Schema):
    id = fields.Integer(dump_only = True)
    time = fields.String(required=True)
    tyre_type = fields.String(required=True)
    fuel = fields.String(required=True)
    bodywork = fields.String(load_only=-True)
    data = fields.Dict(required=False)
    
    @post_load
    def make_vehicle(self, data, **kwargs):
        return Vehicle(**data)