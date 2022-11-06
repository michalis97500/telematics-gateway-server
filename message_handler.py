import json
import re
import database_handler as db


class MessageHandler:
    def __init__(self, DEBUG=False, topic_dict=None):

        self.DEBUG = DEBUG
        self.connection = db.DatabaseHandler('Database.db')

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
                print("Error 6 : Topic is not valid" + str(e))
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
                    print("Error 9 : Parameter is not valid" + str(e))
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
                print("Error 10 : information conversion error " + str(e))
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
                print("Error 11 : Database write error " + str(e))
            return False

    def parameter_handler(self, topic, payload, note="NOT SPECIFIED"):
        '''Handle parameter messages'''
        '''Topic is a json object'''
        # Get timestamp
        timestamp = payload['TM']
        all_good = False
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
                    all_good = True
                else:
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
            print("Error 12 : Navigation message is not valid" + str(e))
            return False

        try:
            if self.connection:
                return self.connection.insert_into_navigation(string)
            return False
        except Exception as e:
            if self.DEBUG:
                print("Error 13 : Database write error " + str(e))
            return False

    def message_handle_method(self, message):
        if message:
            try:
                message_json = json.loads(message, strict=False)
                topic = json.loads(self.topic_to_json(
                    message_json['topic']), strict=False)
                payload = message_json['payload']
                # From the topic determine the type of message

                # if message is a parameter
                if self.topic_dict[topic['packet_type']] == "parameter":
                    return self.parameter_handler(topic, payload, note="PARAMETER")

                # if message is an event
                elif self.topic_dict[topic['packet_type']] == "event":
                    return self.parameter_handler(topic, payload, note="EVENT")

                # if message is an error
                elif self.topic_dict[topic['packet_type']] == "error":
                    return self.error_handler(topic, payload)

                # if message is a group
                elif self.topic_dict[topic['packet_type']] == "group":
                    return self.group_handler(topic, payload)

                # if message is a navigation message
                elif self.topic_dict[topic['packet_type']] == "navigation":
                    return self.navigation_handler(topic, payload, note="NAVIGATION")

                # if message is not valid
                if self.DEBUG:
                    print("Error 7 : Message is not valid" + str(e))

            except KeyError as e:
                if self.DEBUG:
                    print(
                        "Error 8 : Message is not valid, missing key from dictionary" + str(e))
                    return None
            except Exception as e:
                if self.DEBUG:
                    print("Error 7 : Message is not valid" + str(e))
                return None
        return None
