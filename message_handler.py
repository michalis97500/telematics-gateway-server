import json
import re
import database_handler as db
import time

error_dict = {
    1: "Topic not valid",
    2: "Message not valid",
    3: "Message not valid, missing key",
    4: "Parameter not valid",
    5: "Information conversion error",
    6: "Database write error",
    7: "Navigation message not valid",
    8: "Failed to load database configuration file",
    9: "Failed to connect to database",
    10: "Database write error",
}



class MessageHandler:
    def __init__(self, DEBUG=False, db_configuration_file=None):

        self.DEBUG = DEBUG
        
        if db_configuration_file:
            try:
                configuration_settings = self.load_config(db_configuration_file)
            except Exception:
                if self.DEBUG:
                    print('MH Error 8: Failed to load configuration DB file')
        
            try: 
                self.connection = db.DatabaseHandler(database_name=configuration_settings['DB_NAME'],password=configuration_settings['DB_PASSWORD'])
            except Exception:
                if self.DEBUG:
                    print('MH Error 9.1: Failed to connect to database with given settings')
                    
        elif db_configuration_file == None:
            try:
                print("No configuration has been provided for the database")
                db_name = input("Enter the name of the database: ")
                password = getpass(prompt="Enter the password for the database: ")
                self.connection = db.DatabaseHandler(database_name=db_name,password=password)
            except Exception:
                if self.DEBUG:
                    print('MH Error 9.2: Failed to connect to database with given settings')
            
        

        # Topic dictionary, values 1-10 indicate the type of message
        self.topic_dict = {
            1: "parameter",
            2: "parameter",
            3: "parameter",
            4: "parameter",
            5: "parameter",
            6: "parameter",
            7: "event",
            8: "error",
            9: "group",
            10: "navigation"
        }

    def topic_to_json(self, topic):
        '''Identify the topic and return json object'''
        try:
            if isinstance(topic, str):
                array = topic.split("/")
                data = {}
                data['case_id'] = int(array[0].strip())
                data['host_id'] = int(array[1].strip())
                data['md_id'] = int(array[2].strip())
                data['packet_type'] = int(array[3].strip())
                return json.dumps(data)
        except Exception as e:
            if self.DEBUG:
                print("MH Error 1 : Topic is not valid " + str(e))
            return topic

    def information_to_json(self, information, parameter_value, timestamp):
        try:
            '''Gets an array of information from the payload'''
            '''Returns it as a json object'''
            # SA and SPN are ALWAYS found, SPECGR and SPEC are optional and can be 1-3
            # Extract the information
            data = {}
            if (len(information) < 2 or len(information) > 5):  # If the information is not valid
                if self.DEBUG:
                    print("MH Error 4 : Parameter is not valid" + str(e))
                    return None
            data['SA'] = int(information[0])
            data['SVN'] = int(information[1])
            if (len(information) == 2):  # SA and SVN only
                data['SPECGR1_SPEC1'] = float(-1)
                data['SPECGR2_SPEC2'] = float(-1)
                data['SPECGR3_SPEC3'] = float(-1)
            if (len(information) == 3):  # SA and SVN and SPECGR1 and SPEC1
                data['SPECGR1_SPEC1'] = float(information[2])
                data['SPECGR2_SPEC2'] = float(-1)
                data['SPECGR3_SPEC3'] = float(-1)
            if (len(information) == 4):  # SA and SVN and SPECGR1 and SPEC1 and SPECGR2 and SPEC2
                data['SPECGR1_SPEC1'] = float(information[2])
                data['SPECGR2_SPEC2'] = float(information[3])
                data['SPECGR3_SPEC3'] = float(-1)
            # SA and SVN and SPECGR1 and SPEC1 and SPECGR2 and SPEC2 and SPECGR3 and SPEC3
            if (len(information) == 5):
                data['SPECGR1_SPEC1'] = float(information[2])
                data['SPECGR2_SPEC2'] = float(information[3])
                data['SPECGR3_SPEC3'] = float(information[4])
            data['parameter_value'] = int(parameter_value)
            data['timestamp'] = int(timestamp)
            return json.dumps(data)
        except Exception as e:
            if self.DEBUG:
                print("MH Error 5 : information conversion error " + str(e))
            return None

    def write_message_to_db(self, processed_message, processed_topic, note="NOT SPECIFIED"):
        '''Write to the database'''
        '''Processed message is a dictionary'''
        '''Processed topic is a json object'''
        # Require a comma separated list of values
        # String format:  timestamp, case_id, host_id, md_id, packet_type, SA, SVN, SPECGR1_SPEC1, SPECGR2_SPEC2, SPECGR3_SPEC3, parameter_value
        try:
            message = json.loads(processed_message, strict=False)
            topic = processed_topic
            string = str(message['timestamp']) + "," + str(topic['case_id']) + "," + str(topic['host_id']) + "," + str(topic['md_id']) + "," + str(topic['packet_type']) + "," + str(message['SA']) + "," + str(
                message['SVN']) + "," + str(message['SPECGR1_SPEC1']) + "," + str(message['SPECGR2_SPEC2']) + "," + str(message['SPECGR3_SPEC3']) + "," + str(message['parameter_value']) + "," + note
            if self.connection:
                return self.connection.insert_into_messages(string)
            return False
        except Exception as e:
            if self.DEBUG:
                print("MH Error 6 : Database write error " + str(e))
            return False

    def parameter_handler(self, topic, payload, note="NOT SPECIFIED"):
        '''Handle parameter messages'''
        '''Topic is a json object'''
        # Get timestamp
        timestamp = payload['TM']
        all_good = True
        # Key has information about who sent the parameter
        # It is a string of the form SA_SPN_SPECGR1.SPEC1_SPECGR2.SPEC2_SPECGR3.SPEC3
        # Loop through the payload and extract the parameters
        for key in payload.keys():
            if key == "TM":  # Skip the timestamp
                continue
            information = key.split("_")
            processed_message = self.information_to_json(
                information, payload[key], timestamp)
            if processed_message != None:
                if self.write_message_to_db(processed_message, topic, note):
                    continue
                else:
                    all_good = False
        return all_good

    def error_handler(self,topic,payload,note="NOTE SPECIFIED"):
        '''Handle error messages'''
        '''Topic is a json object'''
        # Get timestamp
        timestamp_received = payload[0]['TM']
        all_good = True
        # Key has information about who sent the parameter
        # Keys are TM, SA, SID, and FMI
        # Loop through the payload and extract the parameters
        
        #Check if the error is a single error or a list of errors
        if len(payload) == 1:
            #This means there are no errors
            #Create a message saying there are no errors
            string = str(timestamp_received) + "," + str(topic['case_id']) + "," + str(topic['host_id']) + "," + str(topic['md_id']) + "," + str(topic['packet_type']) + "," + str(-1) + "," + str(-1) + "," + str(-1) + "," + str(-1) + "," + str(-1) + "," + str(-1) + "," + "OK_EVENT"
            if self.connection:
                return self.connection.insert_into_messages(string)
        
        for error in payload[1:]:
            string = str(timestamp_received) + "," + str(topic['case_id']) + "," + str(topic['host_id']) + "," + str(topic['md_id']) + "," + str(topic['packet_type']) + "," + str(error['SA']) + "," + str(error['SID']) + "," + str(error['FMI']) + "," + str(error['TM']) + "," + note
            if self.connection:
                if self.connection.insert_into_malfunctions(string):
                    continue
                else:
                    all_good = False
                    
        return all_good
    
    def group_handler(self,topic,payload):
        '''Handles group messages'''
        '''Sends the message to the correct handler'''
        all_good = True
        for message in payload:
            #Get the packet type
            event_id = list(message.keys())[0]
            information = message[event_id]
            #Modify topic to include the event id, not the general group id
            topic['packet_type'] = int(event_id)
            if not self.message_to_method(topic, information):
                all_good = False
        return all_good
            
                
    def navigation_handler(self, topic, payload, note="NOT SPECIFIED"):
        '''Handle navigation messages'''
        '''Topic is a json object'''
        # Get timestamp
        # Key has information about who sent the parameter
        # In this case there is only LA and LO so we can just use the key
        try:
            string = str(payload['TM']) + "," + str(topic['case_id']) + "," + str(topic['host_id']) + "," + str(
                topic['md_id']) + "," + str(topic['packet_type']) + "," + str(payload['LA']) + "," + str(payload['LO']) + "," + note
        except Exception as e:
            print("MH Error 7 : Navigation message is not valid" + str(e))
            return False

        try:
            if self.connection:
                return self.connection.insert_into_navigation(string)
            return False
        except Exception as e:
            if self.DEBUG:
                print("MH Error 10 : Database write error " + str(e))
            return False
        
    def message_to_method(self,topic,payload):
        # if message is a parameter
        if self.topic_dict[topic['packet_type']] == "parameter":
            return self.parameter_handler(topic, payload, note="PARAMETER")

        # if message is an event
        elif self.topic_dict[topic['packet_type']] == "event":
            return self.parameter_handler(topic, payload, note="EVENT")

        # if message is an error
        elif self.topic_dict[topic['packet_type']] == "error":
            return self.error_handler(topic, payload , note="MALFUNCTION")

        # if message is a group
        elif self.topic_dict[topic['packet_type']] == "group":
            return self.group_handler(topic, payload)

        # if message is a navigation message
        elif self.topic_dict[topic['packet_type']] == "navigation":
            return self.navigation_handler(topic, payload, note="NAVIGATION")
        
        # if message is not valid
        if self.DEBUG:
            print("MH Error 2.1 : Message is not valid" + str(e))
        return False


    def message_handle_method(self, message):
        if message:
            try:
                message_json = json.loads(message, strict=False)
                topic = json.loads(self.topic_to_json(message_json['topic']), strict=False)
                payload = message_json['payload']
                
                #Send to the correct handler
                return self.message_to_method(topic, payload)
            
            except KeyError as e:
                if self.DEBUG:
                    print(
                        "MH Error 3 : Message is not valid, missing key from dictionary" + str(e))
                    return None
            except Exception as e:
                if self.DEBUG:
                    print("MH Error 2.2 : Message is not valid " + str(e))
                return None
        return None
        
        
    def load_config(self, file):
        ''' Load the configuartion file'''
        try:
            with open(file) as f:
                return json.load(f)
        except ValueError as e:
            if self.DEBUG:
                print("DB Load error " + file + " is not a valid JSON file"  + str(e))
        except Exception as e:
            if self.DEBUG:
                print("DB Exception error " + str(e))
            return None
