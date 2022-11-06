from paho.mqtt import client as mqtt_client
import json
import time


class MQTTClient:
    def __init__(self, client_id, topic, broker, port, username, password,DEBUG=False):
        'CLIENT VARIABLES CONSTRUCTION'
        self.client_id = client_id
        self.topic = topic
        self.broker = broker
        self.port = port
        self.username = username
        self.password = password
        self.DEBUG = DEBUG
        self.last_message = None
        
        'CLIENT ON CONNECT CALLBACK'
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Client Error 3 " + "Failed to connect, return code %d\n", rc)
                
        'CLIENT ON MESSAGE CALLBACK'
        def on_message(client, userdata, msg):
            try:
                data = {}
                data['topic'] = msg.topic
                data['payload'] = json.loads(msg.payload,strict=False)
                self.last_message = json.dumps(data)
            except Exception as e:
                self.last_message = '{"topic":"ERROR","payload":"MSG_NOT_VALID_JSON"}'
                if self.DEBUG:
                    print("Client Error 1" + str(e))
        
        'CLIENT FUNCTION INITIALISATION'
        self.client = mqtt_client.Client(client_id)
        
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.username_pw_set(username, password)
        self.client.connect(broker, port)
  
    def get_message(self):
        'Returns the last message received'
        if self.last_message is not None:
            message = self.last_message
            self.last_message = None
            return message
        return None
  
    def publish(self,msg,topic=None):
        'Sends message to the broker'
        'Topic is set as self.topic'
        try:
            if topic is None:
                result = self.client.publish(self.topic, msg)
            if topic :
                result = self.client.publish(topic, msg)
            status = result[0]
            if status == 0:
                return True
            else:
                return False
        except Exception as e:
            if self.DEBUG:
                print("Client Error 2 "  + str(e))
            return False
    
    def subscribe(self,topic=None):
        'Subscribes to a topic'
        'Created in another thread'
        try:
            if topic is None:
                self.client.subscribe(self.topic)
            if topic :
                self.client.subscribe(topic)
            self.client.loop_start()
        except Exception as e:
            if self.DEBUG:
                print("Client Error 4 "  + str(e))

            
        
    def unsubscribe(self,topic=None):
        'Unsubscribes from a topic'
        try:
            if topic is None:
                self.client.unsubscribe(self.topic)
            if topic :
                self.client.unsubscribe(topic)
            return True
        except Exception as e:
            if self.DEBUG:
                print("Client Error 5 "  + str(e))
            return False
        

