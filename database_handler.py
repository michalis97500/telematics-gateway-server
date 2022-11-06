import sqlite3 as sql

#TODO: Encrypted database

class DatabaseHandler:
  
  def __init__(self, database_name):
    self.database_name = database_name
    self.connection = sql.connect(database_name)
    self.cursor = self.connection.cursor()
    
    self.create_default_table()
    
  def create_default_table(self):
    MESSAGES = "CREATE TABLE IF NOT EXISTS MESSAGES (TIMESTAMP INT NOT NULL, CASE_ID INT NOT NULL, HOST_ID INT NOT NULL, MD_ID INT NOT NULL, REPORT_ID INT NOT NULL, SA INT NOT NULL, SVN INT NOT NULL, SPECGR1_SPEC1 INT, SPECGR2_SPEC2 INT, SPECGR3_SPEC3 INT, VALUE INT NOT NULL, NOTE STRING NOT NULL);"
    NAVIGATION = "CREATE TABLE IF NOT EXISTS NAVIGATION (TIMESTAMP INT NOT NULL, CASE_ID INT NOT NULL, HOST_ID INT NOT NULL, MD_ID INT NOT NULL, REPORT_ID INT NOT NULL, LATITUDE INT NOT NULL, LONGITUDE INT NOT NULL, NOTE STRING NOT NULL);"
    MALFUNCTIONS = "CREATE TABLE IF NOT EXISTS MALFUNCTIONS (TIMESTAMP INT NOT NULL, CASE_ID INT NOT NULL, HOST_ID INT NOT NULL, MD_ID INT NOT NULL, REPORT_ID INT NOT NULL, SA INT NOT NULL, SID INT NOT NULL, FMI INT NOT NULL, ERROR_TIMESTAMP INT NOT NULL, NOTE STRING NOT NULL);"
    self.cursor.execute(MESSAGES)
    self.cursor.execute(NAVIGATION)
    self.cursor.execute(MALFUNCTIONS)
    self.connection.commit()
    
  def insert_into_messages(self, message):
    try :
      information = message.split(",")
      self.cursor.execute("INSERT INTO MESSAGES VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (information[0], information[1], information[2], information[3], information[4], information[5], information[6], information[7], information[8], information[9], information[10],information[11]))
      self.connection.commit()
      return True
    except Exception as e:
      print("Error 11 : Database write error " + str(e))
      return False
    
  def insert_into_navigation(self, message):
    try :
      information = message.split(",")
      self.cursor.execute("INSERT INTO NAVIGATION VALUES (?,?,?,?,?,?,?,?)", (information[0], information[1], information[2], information[3], information[4], information[5], information[6], information[7]))
      self.connection.commit()
      return True
    except Exception as e:
      print("Error 12 : Database write error " + str(e))
      return False
      
  def insert_into_malfunctions(self, message):
    try:
      information = message.split(",")
      self.cursor.execute("INSERT INTO MALFUNCTIONS VALUES (?,?,?,?,?,?,?,?,?,?)", (information[0], information[1], information[2], information[3], information[4], information[5], information[6], information[7], information[8], information[9]))
      self.connection.commit()
      return True
    except Exception as e:
      print("Error 13 : Database write error " + str(e))
      return False
    