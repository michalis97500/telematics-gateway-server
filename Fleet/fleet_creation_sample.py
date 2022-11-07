import fleet
import vehicle
import driver


veh1 = vehicle.Vehicle(name="Truck1", model="Nissan F1", year=2019, plates="KMN090", color="White", tank_size=1000)
veh2 = vehicle.Vehicle(name="Truck2", model="Nissan F12", year=2020, plates="KMN091", color="Black", tank_size=500)
veh3 = vehicle.Vehicle(name="Truck3", model="Nissan F13", year=2021, plates="KMN092", color="Magenda", tank_size=1500)

driver1 = driver.Driver(first_name = "Mike",last_name= "Chris",age = 24,license_number= 100234, license_expiration = '18/02/21', vehicle=veh1, driver_id = 1)
driver2 = driver.Driver(first_name = "Mike1",last_name= "Chris1",age = 25,license_number= 100235, license_expiration = '18/02/21', vehicle=veh2, driver_id = 2)
driver3 = driver.Driver(first_name = "Mike2",last_name= "Chris2",age = 26,license_number= 100236, license_expiration = '18/02/21', vehicle=veh3, driver_id = 3)

fleet1 = fleet.Fleet(fleet_id = 1001)
fleet1.add_driver(driver1)
fleet1.add_driver(driver2)
fleet1.add_driver(driver3)
fleet1.add_vehicle(veh1)
fleet1.add_vehicle(veh2)
fleet1.add_vehicle(veh3)
fleet1.save_fleet(filename="fleet1")


for item in fleet1.get_drivers():
  print(item.get_vehicle())
for item in fleet1.get_vehicles():
  print(item)


print("load 2")
fleet2 = fleet.load_fleet(filename="fleet1")

for item in fleet2.get_drivers():
  print(item.get_vehicle())
for item in fleet2.get_vehicles():
  print(item)
  
print(fleet2.get_fleet_id())

print(fleet1.__eq__(fleet2))

