
class Vehicle:
  def __init__(self, name, model, year, plates, color, tank_size):  
    self.name = name
    self.model = model
    self.year = year
    self.plates = plates
    self.color = color
    self.tank_size = tank_size
    self.location = []
    self.fuel_level = 0
    
    
  def __str__(self) -> str:
    return f"Vehicle: {self.name}, {self.model}, {self.year}, {self.plates}, {self.color}, {self.location}, {self.tank_size}, {self.fuel_level}"
  
  def get_name(self) -> str:
    return self.name
  
  def get_model(self) -> str:
    return self.model
  
  def get_year(self) -> int:
    return self.year
  
  def get_plates(self) -> str:
    return self.plates
  
  def get_color(self) -> str:
    return self.color
  
  def get_location(self) -> []:
    return self.location
  
  def set_location(self, latitude, longitude):
    self.location = [latitude, longitude]
    
  def set_tank_size(self, tank_size):
    self.tank_size = tank_size
    
  def get_tank_size(self) -> int:
    return self.tank_size
  
  def get_fuel_level(self) -> int:
    return self.fuel_level
  
  def set_fuel_level(self, fuel_level):
    self.fuel_level = fuel_level
  
  def get_all_info(self) -> []:
    return [self.name, self.model, self.year, self.plates, self.color, self.location, self.tank_size, self.fuel_level]
  
  def get_vehicle_id(self) -> int:
    return self.vehicle_id
  
  def set_vehicle_id(self, vehicle_id):
    self.vehicle_id = vehicle_id
  
  