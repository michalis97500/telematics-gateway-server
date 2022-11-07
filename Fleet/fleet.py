import driver
import vehicle
import pickle
import os

default_location = '\Fleet\Backup\\'

class Fleet:
  def __init__(self, fleet_id):
    self.drivers, self.vehicles = [], []
    self.fleet_id = fleet_id
    
  def track_driver(self, driver_id):
    for driver in self.drivers:
      if driver.get_driver_id() == driver_id:
        return driver.get_vehicle().get_location()
    return None
  
  def track_vehicle(self, vehicle_id):
    for vehicle in self.vehicles:
      if vehicle.get_vehicle_id() == vehicle_id:
        return vehicle.get_location()
    return None
  
  def track_fleet(self):
    location_list = []
    for vehicle in self.vehicles:
      location_list.append([vehicle.get_location() , vehicle.get_vehicle_id()])
    return location_list
      
  def get_drivers(self):
    return self.drivers
  
  def get_vehicles(self):
    return self.vehicles
  
  def get_fleet_id(self):
    return self.fleet_id
  
  def add_driver(self, driver):
    self.drivers.append(driver)
    
  def add_vehicle(self, vehicle):
    self.vehicles.append(vehicle)
    
  def remove_driver(self, driver_id):
    for driver in self.drivers:
      if driver.get_driver_id() == driver_id:
        self.drivers.remove(driver)
        return True
    return False
  
  def remove_vehicle(self, vehicle_id):
    for vehicle in self.vehicles:
      if vehicle.get_vehicle_id() == vehicle_id:
        self.vehicles.remove(vehicle)
        return True
    return False
  
  def save_fleet(self, filename, location=os.getcwd()+ default_location ):
    filename = location + filename
    #save the fleet to a file
    with open(filename + "_drivers", 'wb') as file:
      pickle.dump(self.get_drivers(), file)
      file.close()
    with open(filename + "_vehicles", 'wb') as file:
      pickle.dump(self.get_vehicles(), file)
      file.close()
    with open(filename + "_fleet", 'wb') as file:
      pickle.dump(self, file)
      file.close()
      
  def __eq__(self, other) : 
    return self.__dict__ == other.__dict__

  def load_drivers_from_file(self, filename, location=os.getcwd()+ default_location):
    filename = location + filename
    with open(filename + "_drivers", 'rb') as file:
      self.drivers = pickle.load(file)
      file.close()

  def load_vehicles_from_file(self, filename, location=os.getcwd()+ default_location):
    filename = location + filename
    with open(filename + "_vehicles", 'rb') as file:
      self.vehicles = pickle.load(file)
      file.close()
      
def load_fleet(filename, location=os.getcwd()+ default_location ):
  filename = location + filename
  with open(filename + "_fleet", 'rb') as file:
    fleet = (pickle.load(file))
    file.close()
  return fleet
