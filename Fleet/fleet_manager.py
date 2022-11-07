import fleet
import vehicle
import driver
import sqlite3
import database_handler as db

connection = db.DatabaseHandler('Database.db')

def update_vehicle_locations(fleet):
  for vehicle in fleet.get_vehicles():
    #TODO: Update the vehicle location
    some_var = vehicle.get_vehicle_id()
    #use some_var to get location from database
    if connection:
      latitude, longitude = connection.get_vehicle_location(some_var)
      vehicle.set_location(latitude,longitude)