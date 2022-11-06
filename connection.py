import mqtt_client
import json
import os
import time

DEBUG = True
broker_config = os.getcwd()+r'\config\broker.json'


def load_config(file):
    ''' Load the configuartion file'''
    try:
        with open(file) as f:
            return json.load(f)
    except ValueError as e:
        if DEBUG:
            print("Error 2 " + file + " is not a valid JSON file"  + str(e))
    except Exception as e:
        if DEBUG:
            print("Error 1 " + str(e))
        return None


def initiate_connection(configuration) -> mqtt_client.MQTTClient:
    '''Initiate a connection and return client object if successful'''
    try:
        configuration_settings = load_config(configuration)
    except Exception as e:
        if DEBUG:
            print('Failed to load configuration file')
        return None

    try:
        if configuration_settings:
            client = mqtt_client.MQTTClient(configuration_settings['client_id'], 
                                            configuration_settings['topic'], 
                                            configuration_settings['broker_address'],
                                            configuration_settings['broker_port'], 
                                            configuration_settings['username'], 
                                            configuration_settings['password'], 
                                            DEBUG=DEBUG)
            return client
        else:
            return None
    except Exception as e:
        if DEBUG:
            print("Error 3 "  + str(e))
        return None

def default_connection() -> mqtt_client.MQTTClient:
    try:
        client = initiate_connection(broker_config)
        if client:
            return client
        else:
            if DEBUG:
                print("Error 4" + 'Failed to initiate client object'  + str(e))
            return None
    except Exception as e:
        if DEBUG:
            print("Error 5 : Check connection" + str(e))
        return None

