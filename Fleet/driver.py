import vehicle

class Driver:
  def __init__(self, first_name, last_name, age, license_number, license_expiration, vehicle, driver_id):
    #Create a driver object
    self.first_name = first_name
    self.last_name = last_name
    self.age = age
    self.license_number = license_number
    self.licence_exp = license_expiration
    self.vehicle = vehicle
    self.driver_id = driver_id
    
    
  def __str__(self) -> str:
    return f"Driver: {self.first_name}, {self.last_name}, {self.age}, {self.license_number}, {self.licence_exp}, {self.vehicle}, {self.driver_id}"
  
  def get_first_name(self) -> str:
    return self.first_name
  
  def get_last_name(self) -> str:
    return self.last_name
  
  def get_age(self) -> int:
    return self.age
  
  def get_license_number(self) -> str:
    return self.license_number
  
  def get_license_expiration(self) -> str:
    return self.licence_exp
  
  def get_vehicle(self):
    return self.vehicle
  
  def get_driver_id(self) -> int:
    return self.driver_id
  
  def set_vehicle(self, vehicle):
    self.vehicle = vehicle
  
  def get_all_info(self) -> []:
    return [self.first_name, self.last_name, self.age, self.license_number, self.licence_exp, self.vehicle, self.driver_id]