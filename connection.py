import mqtt_client
import json
import os

_DEBUG = False

def connect(default=False, configuration=None,  DEBUG=False) -> mqtt_client.MQTTClient:
    '''Connect to the broker and return client object if successful'''
    global _DEBUG
    _DEBUG = DEBUG
    if default:
        return default_connection()
    elif configuration:
        return initiate_connection(configuration)
    else:
        if _DEBUG:
            print("Error 6 : No configuration file provided")
        return None


def load_config(file):
    ''' Load the configuartion file'''
    try:
        with open(file) as f:
            return json.load(f)
    except ValueError as e:
        if _DEBUG:
            print("Error 2 " + file + " is not a valid JSON file"  + str(e))
    except Exception as e:
        if _DEBUG:
            print("Error 1 " + str(e))
        return None


def initiate_connection(configuration) -> mqtt_client.MQTTClient:
    '''Initiate a connection and return client object if successful'''
    try:
        configuration_settings = load_config(configuration)
    except Exception as e:
        if _DEBUG:
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
                                            DEBUG=_DEBUG)
            return client
        else:
            return None
    except Exception as e:
        if _DEBUG:
            print("Error 3 "  + str(e))
        return None

def default_connection() -> mqtt_client.MQTTClient:
    try:
        client = initiate_connection(os.getcwd()+r'\config\broker.json')
        if client:
            return client
        else:
            if _DEBUG:
                print("Error 4" + 'Failed to initiate client object'  + str(e))
            return None
    except Exception as e:
        if _DEBUG:
            print("Error 5 : Check connection" + str(e))
        return None

