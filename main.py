import connection as cn
import message_handler as mh
import os

error_dict = {
  1: "Cannot start main loop",
}

def main():
  
  try:
    # Create a connection object
    connection = cn.connect(default=True,DEBUG=True)
    if connection is None:
      print("No connection was established")
      os._exit(1)
    # Create a message handler object
    _message_handler = mh.MessageHandler(db_configuration_file = os.getcwd()+r'\config\database.json' , DEBUG=True)
    #Connect to the broker
    if type(connection) == cn.mqtt_client.MQTTClient:
      # Subscribe to the topic
      connection.subscribe(topic='#')
      while True:
        # Get the message and handle it
        handled = _message_handler.message_handle_method(connection.get_message())
        if handled:
          print("Message received and handled")
        elif handled == False:
            print("Message not handled")
  except Exception as e:
    print("Error 1 : " + str(e))
          
main()