from .vehicle_model import Vehicle
class VehicleBuilder:
    def __init__(self, time, tyre_type, fuel, bodywork):
        self.vehicle = Vehicle()
        self.vehicle.time = time
        self.vehicle.tyre_type = tyre_type
        self.vehicle.fuel = fuel
        self.vehicle.bodywork = bodywork


    def build(self):
        return self.user